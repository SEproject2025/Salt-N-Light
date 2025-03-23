# Standard library imports
import logging

# Third-party imports
# pylint: disable=C0412
from rest_framework import generics, filters, views, response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
# pylint: enable=C0412

# Django imports
from django.db.models import Q
from django.core.exceptions import ValidationError, ObjectDoesNotExist, \
                                   PermissionDenied
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment, \
    ProfileTagging, Notification
from .serializer import TagSerializer, SearchHistorySerializer, \
    ExternalMediaSerializer, \
    ProfileSerializer, ProfileVoteSerializer,\
    ProfileCommentSerializer, NotificationSerializer

# Set up logging
logger = logging.getLogger(__name__)

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
   queryset = (
      Profile.objects
      .select_related('user')
      .prefetch_related('tags')
      .all()
   )
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing

   def get_serializer_context(self):
      context = super().get_serializer_context()
      context['profile_id'] = self.kwargs.get('pk')
      return context

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
   permission_classes = [AllowAny]  # Allow public access

   def get_permissions(self):
      if self.action in ['create', 'update', 'partial_update', 'destroy']:
         return [IsAuthenticated()]
      return [AllowAny()]

   @action(detail=False, methods=['post'], url_path='add-to-profile',
   url_name='add_to_profile')
   def add_to_profile(self, request):
      profile_id = request.data.get('profile_id')
      tag_id = request.data.get('tag_id')
      if not profile_id or not tag_id:
         return Response(
            {'error': 'Both profile_id and tag_id are required'},
            status=status.HTTP_400_BAD_REQUEST
         )

      try:
         profile = Profile.objects.get(user_id=profile_id)
         tag = Tag.objects.get(id=tag_id)

         # Check if the tag already exists on the profile
         existing_tag = ProfileTagging.objects.filter(
            profile=profile,
            tag=tag
         ).first()

         if existing_tag:
            return Response(
               {'error': 'This tag is already added to the profile'},
               status=status.HTTP_400_BAD_REQUEST
            )

         # A tag is self-added if the user is adding it to their own profile
         is_self_added = request.user.id == profile.user.id

         # Create the ProfileTagging instance
         ProfileTagging.objects.create(
            profile=profile,
            tag=tag,
            added_by=request.user,
            is_self_added=is_self_added
         )

         return Response({
            'message': f'Tag "{tag.tag_name}" added to profile successfully',
            'tag_id': tag.id,
            'profile_id': profile_id,
            'is_self_added': is_self_added,
            'added_by': request.user.id
         }, status=status.HTTP_200_OK)

      except ObjectDoesNotExist:
         return Response( # pylint: disable=eval-used
            {'error': 'Profile or Tag not found'},
            status=status.HTTP_404_NOT_FOUND
         )

      except ValidationError as e:
         return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
         )

   @action(detail=False, methods=['post'], url_path='remove-from-profile',
   url_name='remove_from_profile')
   # pylint: disable=too-many-return-statements
   def remove_from_profile(self, request):
      profile_id = request.data.get('profile_id')
      tag_id = request.data.get('tag_id')

      if not profile_id or not tag_id:
         return Response(
            {'error': 'Both profile_id and tag_id are required'},
            status=status.HTTP_400_BAD_REQUEST
         )

      try:
         profile = Profile.objects.get(user_id=profile_id)
         tag = Tag.objects.get(id=tag_id)

         # Get the tagging instance
         tagging = ProfileTagging.objects.filter(
            profile=profile,
            tag=tag
         ).first()

         if not tagging:
            return Response(
               {'error': 'Tag not found on this profile'},
               status=status.HTTP_404_NOT_FOUND
            )

         # Safely check if it's a self-added tag
         try:
            is_self_added = tagging.is_self_added
         except AttributeError:
            is_self_added = False

         # Safely get the user who added the tag
         try:
            added_by_id = tagging.added_by.id if tagging.added_by else None
         except AttributeError:
            added_by_id = None

         # First check if it's a self-added tag
         if is_self_added and request.user.id != profile.user.id:
            return Response(
               {'error':
               'Cannot remove tags that users added to their own profile'},
               status=status.HTTP_403_FORBIDDEN
            )

         # Then check if the user has permission to remove the tag
         if (
            not is_self_added
            and added_by_id != request.user.id
            and request.user.id != profile.user.id
         ):
            return Response(
               {'error': 'You can only remove tags you added'},
               status=status.HTTP_403_FORBIDDEN
            )

         tagging.delete()

         return Response({
            'message': f'Tag "{tag.tag_name}" removed from profile.',
            'tag_id': tag.id,
            'profile_id': profile_id
         }, status=status.HTTP_200_OK)

      except ObjectDoesNotExist as e:
         logger.error("Profile not found: %s", e)
         return Response(
            {'error': 'Profile or Tag not found'},
            status=status.HTTP_404_NOT_FOUND
         )

      except ValidationError as e:
         return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
         )
      except PermissionDenied as e:
         print(f"Error in remove_from_profile: {str(e)}")
         return Response(
            {'error': 'Cannot remove this tag'},
            status=status.HTTP_403_FORBIDDEN
         )

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
      # Fetch the user's profile with prefetched tags
      user_profile = (Profile.objects
         .filter(user=request.user)
         .select_related('user')
         .prefetch_related(
            'tags',
            'profile_taggings'  # Need this for is_self_added info
         )
         .first())

      if user_profile:
         # Create context with request and profile_id, matching ProfileDetailView
         context = {
            'request': request,
            'profile_id': user_profile.user.id  # This is crucial for TagSerializer
         }
         serializer = ProfileSerializer(user_profile, context=context)
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
      # Start with base queryset and
      # exclude profiles without a user_type or anonymous profiles
      queryset = (Profile.objects
                 .select_related('user')
                 .prefetch_related('tags')
                 .exclude(user_type__isnull=True)
                 .exclude(user_type='')
                 .exclude(user_type='anonymous'))

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
               Q(description__icontains=search_query) |
               Q(street_address__icontains=search_query) |
               Q(city__icontains=search_query) |
               Q(state__icontains=search_query) |
               Q(country__icontains=search_query)
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


class NotificationView(ModelViewSet):
   serializer_class = NotificationSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
      # Only return notifications for the current user
      return Notification.objects.filter(recipient=self.request.user)

   def perform_create(self, serializer):
      # Set the recipient as the current user when creating a notification
      serializer.save(recipient=self.request.user)
