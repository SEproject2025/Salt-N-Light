from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters, views, response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment
from .serializer import TagSerializer, SearchHistorySerializer, \
    ExternalMediaSerializer, \
    ProfileSerializer, ProfileVoteSerializer, ProfileCommentSerializer
from rest_framework.pagination import PageNumberPagination


class ProfileListCreateView(generics.ListCreateAPIView):
   queryset = Profile.objects.select_related(
      'user').prefetch_related('tags').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing
   filter_backends = [filters.SearchFilter]
   search_fields = ['user_type', 'city', 'state', 'country', 'denomination']
   filterset_fields = ['user_type', 'city', 'state', 'country',
                       'denomination', 'tags']


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Profile.objects.select_related('user').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing


class MatchmakingResultsView(generics.ListAPIView):
   serializer_class = ProfileSerializer
   authentication_classes = [JWTAuthentication]
   # Only authenticated users can access
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
      user_profile = Profile.objects.filter(
         user=self.request.user).prefetch_related('tags').first()

      if not user_profile:
         return Profile.objects.none()
         # Return an empty queryset if the user has no profile

      # Get the tags associated with the current user's profile
      user_tags = user_profile.tags.all()

      # Find profiles with at least one matching tag, excluding
      # the current user's profile
      matching_profiles = Profile.objects.filter(
         Q(tags__in=user_tags)).exclude(
          user=self.request.user).distinct()

      return matching_profiles.exclude(user_type=user_profile.user_type)

# Tag viewset that performs CRUD operations


class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name', 'tag_description', 'tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [AllowAny]

# Search history viewset that performs CRUD operations


class SearchHistoryViewSet(ModelViewSet):
   queryset = SearchHistory.objects.all()
   serializer_class = SearchHistorySerializer
   permission_classes = [AllowAny]

# External media viewset that performs CRUD operations


class ExternalMediaViewSet(ModelViewSet):
   queryset = ExternalMedia.objects.all()
   serializer_class = ExternalMediaSerializer
   permission_classes = [AllowAny]

# View for retrieving the currently logged in user


class CurrentUserView(views.APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request):
      # Fetch the user's profile in the same way as MatchmakingResultsView
      user_profile = Profile.objects.filter(
         user=request.user
      ).select_related('user').prefetch_related('tags').first()

      if user_profile:
         serializer = ProfileSerializer(user_profile)
         return response.Response(serializer.data)

      return response.Response({"error": "Profile not found"}, status=404)


class ProfileVoteView(generics.CreateAPIView, generics.UpdateAPIView):
   serializer_class = ProfileVoteSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def create(self, request, *args, **kwargs):
      profile_id = request.data.get('profile')
      is_upvote = request.data.get('is_upvote')

      # Check if vote already exists
      existing_vote = ProfileVote.objects.filter(
          voter=request.user,
          profile_id=profile_id
      ).first()

      if existing_vote:
         # Update existing vote
         existing_vote.is_upvote = is_upvote
         existing_vote.save()
         serializer = self.get_serializer(existing_vote)
         return response.Response(serializer.data)

      # Create new vote
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileCommentView(generics.CreateAPIView, generics.UpdateAPIView):
   serializer_class = ProfileCommentSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]
   queryset = ProfileComment.objects.all()

   def create(self, request, *args, **kwargs):
      # Check if user has already commented
      profile_id = request.data.get('profile')
      existing_comment = ProfileComment.objects.filter(
          commenter=request.user,
          profile_id=profile_id
      ).exists()

      if existing_comment:
         return response.Response(
             {"error": "You have already commented on this profile"},
             status=status.HTTP_400_BAD_REQUEST
         )

      # Check if user has voted
      has_voted = ProfileVote.objects.filter(
          voter=request.user,
          profile_id=profile_id
      ).exists()

      if not has_voted:
         return response.Response(
             {"error": "You must vote before commenting"},
             status=status.HTTP_400_BAD_REQUEST
         )

      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return response.Response(serializer.data, status=status.HTTP_201_CREATED)

   def update(self, request, *args, **kwargs):
      comment = self.get_object()

      # Check if the user is the owner of the comment
      if comment.commenter != request.user:
         return response.Response(
             {"error": "You can only edit your own comments"},
             status=status.HTTP_403_FORBIDDEN
         )

      serializer = self.get_serializer(
         comment, data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)

      return response.Response(serializer.data)

   def perform_create(self, serializer):
      serializer.save(commenter=self.request.user)


class ProfileVoteStatusView(views.APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request, profile_id):
      vote = ProfileVote.objects.filter(
          voter=request.user,
          profile_id=profile_id
      ).first()

      return response.Response({
          'has_voted': vote is not None,
          'is_upvote': vote.is_upvote if vote else None
      })


class ProfileSearchView(generics.ListAPIView):
   serializer_class = ProfileSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]
   pagination_class = PageNumberPagination

   def get_queryset(self):
      queryset = Profile.objects.select_related('user').prefetch_related(
         'tags'
      )

      # Get search parameters from query string
      search_query = self.request.query_params.get('q', '')
      user_type = self.request.query_params.get('user_type', '')
      tags = self.request.query_params.getlist('tags', [])
      location = self.request.query_params.get('location', '')
      sort = self.request.query_params.get('sort', 'recent')

      # Apply sorting
      if sort == 'recent':
         queryset = queryset.order_by('-user_id')  # Most recent users first
      elif sort == 'name':
         queryset = queryset.order_by('first_name', 'last_name')
      elif sort == 'location':
         queryset = queryset.order_by('country', 'state', 'city')

      # Only apply filters if search parameters are provided
      if any([search_query, user_type, tags, location]):
         if search_query:
            queryset = queryset.filter(
               Q(first_name__icontains=search_query) |
               Q(last_name__icontains=search_query) |
               Q(description__icontains=search_query)
            )

         if user_type:
            queryset = queryset.filter(user_type=user_type)

         if tags:
            queryset = queryset.filter(tags__tag_name__in=tags).distinct()

         if location:
            queryset = queryset.filter(
               Q(street_address__icontains=location) |
               Q(city__icontains=location) |
               Q(state__icontains=location) |
               Q(country__icontains=location)
            )

      return queryset

   def list(self, request, *args, **kwargs):
      # Get the page size from query params, default to 'all'
      page_size = request.query_params.get('page_size', 'all')
      
      # Handle 'all' option (now the default)
      if page_size == 'all':
         queryset = self.get_queryset()
         serializer = self.get_serializer(queryset, many=True)
         return response.Response({
            'count': len(serializer.data),
            'next': None,
            'previous': None,
            'results': serializer.data
         })
      
      # Set the page size for pagination if a specific size is requested
      try:
         self.pagination_class.page_size = int(page_size)
      except ValueError:
         # If invalid page size, default to showing all
         queryset = self.get_queryset()
         serializer = self.get_serializer(queryset, many=True)
         return response.Response({
            'count': len(serializer.data),
            'next': None,
            'previous': None,
            'results': serializer.data
         })
      
      return super().list(request, *args, **kwargs)
