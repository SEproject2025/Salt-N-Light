# Standard library imports
import logging

# Third-party imports
# pylint: disable=C0412
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters, views, response, status
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
    ProfileTagging, Notification, Friendship
from .serializer import TagSerializer, SearchHistorySerializer, \
    ExternalMediaSerializer, \
    ProfileSerializer, ProfileVoteSerializer,\
    ProfileCommentSerializer, NotificationSerializer, FriendshipSerializer, \
    ProfileSearchSerializer
from django.db.models import Case, When, IntegerField
from django.conf import settings

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

class FriendshipViewSet(ModelViewSet):
   serializer_class = FriendshipSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   # Define the queryset
   queryset = Friendship.objects.all()

   def perform_create(self, serializer):
      # Check if the user is authenticated
      if not self.request.user.is_authenticated:
         raise PermissionDenied("You must log in to send a friend request.")

      # Set the sender as the current user
      serializer.save(sender=self.request.user)

      # Create a notification for the receiver
      Notification.objects.create(
         recipient=serializer.validated_data['receiver'],
         notification_type='friend_request',
         message=f"{self.request.user.username} sent you a friend request",
         related_object_id=serializer.instance.id
      )

   @action(detail=True, methods=['post'])
   def respond(self, request, pk=None): # pylint: disable=unused-argument

      try:
         friendship = self.get_object()
         print(f"Found friendship: {friendship}")

         response_action = request.data.get('action')
         print(f"Action received: {response_action}")

         if response_action == 'accept':
            friendship.status = 'accepted'
         elif response_action == 'reject':
            friendship.status = 'rejected'
         else:
            return Response(
               {"error": "Invalid action"},
               status=status.HTTP_400_BAD_REQUEST
            )

         friendship.save()
         return Response({
            "message": f"Friend request {response_action}ed successfully"
         }, status=status.HTTP_200_OK)
      except ObjectDoesNotExist:
         return Response(
            {"error": "Friendship not found"},
            status=status.HTTP_404_NOT_FOUND
         )
      except ValidationError as e:
         return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
         )

   @action(detail=False, methods=['get'])
   def status(self, request, profile_id=None):
      try:
         if not profile_id:
            return Response({'error': 'Profile ID is required'},
                          status=status.HTTP_400_BAD_REQUEST)

         # Get the friendship between the current user and the specified profile
         friendship = Friendship.objects.filter(
             Q(sender=request.user, receiver_id=profile_id) |
             Q(sender_id=profile_id, receiver=request.user)
         ).first()

         print(f"Found friendship: {friendship}")  # Debug log

         if friendship:
            response_data = {
                'status': friendship.status,
                'friendship_id': friendship.id,
                'is_sender': friendship.sender == request.user
            }
            print(f"Returning response: {response_data}")  # Debug log
            return Response(response_data)
         print("No friendship found")  # Debug log
         return Response({'status': None})
      except (ObjectDoesNotExist, ValidationError) as e:
         print(f"Error in status method: {str(e)}")  # Debug log
         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileSearchView(generics.ListAPIView):
   serializer_class = ProfileSearchSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]
   pagination_class = PageNumberPagination

   def get_queryset(self):
      # Start with base queryset and optimize with select_related and prefetch_related
      queryset = (Profile.objects
                 .select_related('user')
                 .prefetch_related('tags', 'votes_received')
                 .exclude(user_type__isnull=True)
                 .exclude(user_type='')
                 .exclude(user_type='anonymous'))

      # Get search parameters from query string
      search_query = self.request.query_params.get('q', '').strip()
      user_type = self.request.query_params.get('user_type', '').strip()
      tags = self.request.query_params.getlist('tags', [])
      location = self.request.query_params.get('location', '').strip()
      sort = self.request.query_params.get('sort', 'recent')

      # Build search filters
      filters = Q()

      # Apply text search if provided
      if search_query:
         search_terms = search_query.split()
         for term in search_terms:
            term_filter = (
               Q(first_name__icontains=term) |
               Q(last_name__icontains=term) |
               Q(description__icontains=term) |
               Q(city__icontains=term) |
               Q(state__icontains=term) |
               Q(country__icontains=term)
            )
            filters &= term_filter

      # Apply user type filter
      if user_type:
         filters &= Q(user_type=user_type)

      # Apply location search if provided
      if location:
         location_terms = location.split()
         location_filter = Q()
         for term in location_terms:
            location_filter |= (
               Q(city__icontains=term) |
               Q(state__icontains=term) |
               Q(country__icontains=term)
            )
         filters &= location_filter

      # Apply filters to queryset
      if filters:
         queryset = queryset.filter(filters)

      # Apply tag filtering if provided
      if tags:
         tag_match_type = self.request.query_params.get('tag_match_type', 'any')
         if tag_match_type == 'all':
            # Match all tags (AND)
            for tag in tags:
               queryset = queryset.filter(tags__tag_name=tag)
         else:
            # Match any tag (OR)
            queryset = queryset.filter(tags__tag_name__in=tags)
         queryset = queryset.distinct()

      # Apply sorting
      if sort == 'recent':
         queryset = queryset.order_by('-created_at')
      elif sort == 'name':
         queryset = queryset.order_by('first_name', 'last_name')
      elif sort == 'location':
         queryset = queryset.order_by('country', 'state', 'city')
      elif sort == 'relevance' and search_query:
         # If sorting by relevance and there's a search query,
         # prioritize exact matches in name fields
         queryset = queryset.annotate(
            name_match=Case(
               When(first_name__iexact=search_query, then=2),
               When(last_name__iexact=search_query, then=2),
               When(first_name__icontains=search_query, then=1),
               When(last_name__icontains=search_query, then=1),
               default=0,
               output_field=IntegerField(),
            )
         ).order_by('-name_match', '-created_at')

      return queryset

   def list(self, request, *args, **kwargs):
      try:
         # Get page size from query params, default to 12
         page_size = request.query_params.get('page_size', 12)
         try:
            page_size = min(int(page_size), getattr(settings, 'MAX_PAGE_SIZE', 100))
         except (TypeError, ValueError):
            page_size = 12

         # Set pagination
         self.pagination_class.page_size = page_size

         # Get queryset and paginate
         queryset = self.get_queryset()
         page = self.paginate_queryset(queryset)
         
         if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

         # If no pagination requested, return all results
         serializer = self.get_serializer(queryset, many=True)
         return Response({
            'count': len(serializer.data),
            'results': serializer.data
         })

      except Exception as e:
         logger.error(f"Error in profile search: {str(e)}")
         return Response(
            {'error': 'An error occurred while processing your search request'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )
