# Standard library imports
import logging
import operator
from functools import reduce

# Third-party imports
# pylint: disable=C0412
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, filters, views, response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
# pylint: enable=C0412

# Django imports
from django.db.models import Q
from django.core.exceptions import ValidationError, ObjectDoesNotExist, \
    PermissionDenied
from django.contrib.auth.models import User
from django.db.utils import DatabaseError
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment, \
    ProfileTagging, Notification, Friendship
from .serializer import TagSerializer, SearchHistorySerializer, \
    ExternalMediaSerializer, \
    ProfileSerializer, ProfileVoteSerializer, \
    ProfileCommentSerializer, NotificationSerializer, FriendshipSerializer, \
    AdminProfileCommentSerializer, AdminProfileSerializer, \
    SearchProfileSerializer

# Set up logging
logger = logging.getLogger(__name__)


# Custom pagination class for admin views
class AdminPagination(PageNumberPagination):
   page_size = 20
   page_size_query_param = 'page_size'
   max_page_size = 100


class ProfileListCreateView(generics.ListCreateAPIView):
   queryset = Profile.objects.select_related(
      'user').prefetch_related('tags').all()
   serializer_class = ProfileSerializer
   permission_classes = [AllowAny]  # Public access for testing
   filter_backends = [filters.SearchFilter]
   search_fields = ['user_type', 'city', 'state', 'country']
   filterset_fields = ['user_type', 'city', 'state', 'country',
                       'tags']

   def get_queryset(self):
      # Get the base queryset
      queryset = super().get_queryset()
      # Filter out anonymous profiles
      queryset = queryset.exclude(is_anonymous=True)
      return queryset


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
      # the current user's profile and anonymous profiles
      matching_profiles = Profile.objects.filter(
         Q(tags__in=user_tags)
      ).exclude(
         Q(user=self.request.user) | Q(is_anonymous=True)
      ).distinct()

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
   def respond(self, request, pk=None):  # pylint: disable=unused-argument

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


# Admin API views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_superuser(request):
   """Check if the current user is a superuser"""
   is_superuser = request.user.is_superuser
   return Response({'is_superuser': is_superuser})


class AdminProfileListView(generics.ListAPIView):
   """List all profiles for admin purposes"""
   serializer_class = AdminProfileSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated, IsAdminUser]
   # Add pagination
   pagination_class = AdminPagination

   def get_queryset(self):
      return Profile.objects.select_related('user').prefetch_related(
         'tags').order_by('user__username').all()


class AdminProfileDeleteView(generics.DestroyAPIView):
   """Delete a profile and all related data"""
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated, IsAdminUser]

   def destroy(self, request, *args, **kwargs):
      try:
          # Get the user ID from the URL
         user_id = kwargs.get('pk')

         # Get the user
         user = User.objects.get(id=user_id)

         # Delete the user (this will cascade delete profile and other related
         # objects)
         user.delete()

         return Response(status=status.HTTP_204_NO_CONTENT)
      except ObjectDoesNotExist:
         return Response(
             {'error': 'User not found'},
             status=status.HTTP_404_NOT_FOUND
         )
      except (ValidationError, PermissionDenied) as e:
         return Response(
             {'error': str(e)},
             status=status.HTTP_400_BAD_REQUEST
         )
      except DatabaseError as e:
         return Response(
             {'error': f'Database error: {str(e)}'},
             status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )


class AdminCommentListView(generics.ListAPIView):
   """List all comments for admin purposes"""
   serializer_class = AdminProfileCommentSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated, IsAdminUser]
   # Add pagination
   pagination_class = AdminPagination

   def get_queryset(self):
      return ProfileComment.objects.select_related(
          'commenter', 'profile', 'profile__user'
      ).order_by('-created_at').all()


class AdminCommentDeleteView(generics.DestroyAPIView):
   """Delete a specific comment"""
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated, IsAdminUser]
   queryset = ProfileComment.objects.all()

   def destroy(self, request, *args, **kwargs):
      try:
         comment = self.get_object()
         comment.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
      except ObjectDoesNotExist:
         return Response(
             {'error': 'Comment not found'},
             status=status.HTTP_404_NOT_FOUND
         )
      except (ValidationError, PermissionDenied) as e:
         return Response(
             {'error': str(e)},
             status=status.HTTP_400_BAD_REQUEST
         )
      except DatabaseError as e:
         return Response(
             {'error': f'Database error: {str(e)}'},
             status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )

class ProfileFilter(FilterSet):
   tags = CharFilter(method='filter_tags')

   def filter_tags(self, queryset, value):
      if not value:
         return queryset
      tag_ids = [int(id) for id in value.split(',') if id.strip().isdigit()]
      return queryset.filter(tags__id__in=tag_ids)

   class Meta:
      model = Profile
      fields = ['user_type', 'city', 'state', 'country']

class ProfileSearchView(generics.ListAPIView):
   serializer_class = SearchProfileSerializer
   permission_classes = [AllowAny]
   filter_backends = [DjangoFilterBackend, filters.SearchFilter]
   filterset_class = ProfileFilter
   search_fields = [
      'user_type', 'city', 'state', 'country', 'tags__tag_name',
      'first_name', 'last_name', 'description'
   ]

   def get_queryset(self):
      logger.info("Starting search with params: %s",
                  self.request.query_params)

      # Log all query parameters
      for key, value in self.request.query_params.items():
         logger.info("Query param - %s: %s", key, value)

      # Build queryset with detailed logging
      logger.info("Building base queryset...")
      queryset = Profile.objects.select_related('user').prefetch_related(
         'tags'
      )
      logger.info("Base queryset count: %s", queryset.count())

      # Apply anonymous filter
      logger.info("Applying anonymous filter...")
      queryset = queryset.exclude(is_anonymous=True)
      logger.info("After anonymous filter count: %s", queryset.count())

      # Log search parameters if present
      search_term = self.request.query_params.get('search', None)
      if search_term:
         logger.info("Search term: %s", search_term)

      # Log filter parameters
      for field in self.filterset_class.Meta.fields + ['tags']:
         value = self.request.query_params.get(field)
         if value:
            logger.info("Filter %s: %s", field, value)

      # Log final queryset SQL
      logger.info("Final queryset SQL: %s", str(queryset.query))

      return queryset

   def get_serializer_context(self):
      context = super().get_serializer_context()
      context['request'] = self.request
      if self.request.user.is_authenticated:
         try:
            profile = Profile.objects.get(user=self.request.user)
            context['profile_id'] = profile.user.id
            logger.info(
               "Added profile_id %s to context for user %s",
               profile.user.id, self.request.user.id)
         except ObjectDoesNotExist:
            logger.warning("Profile not found for user %s",
               self.request.user.id)
      return context

   def list(self, request, *args, **kwargs):
      logger.info("Starting search request from IP: %s",
         request.META.get('REMOTE_ADDR'))
      logger.info("Request headers: %s", request.headers)

      # Get the queryset
      queryset = self.get_queryset()
      logger.info("Queryset count before filtering: %s", queryset.count())

      # Apply filters
      queryset = self.filter_queryset(queryset)
      logger.info("Queryset count after filtering: %s", queryset.count())

      # Paginate
      page = self.paginate_queryset(queryset)
      if page is not None:
         logger.info("Paginated results count: %s", len(page))
         serializer = self.get_serializer(page, many=True)
         return self.get_paginated_response(serializer.data)

      # Serialize
      serializer = self.get_serializer(queryset, many=True)
      logger.info("Serialized results count: %s", len(serializer.data))

      return Response(serializer.data)

class DedicatedSearchView(generics.ListAPIView):
   serializer_class = SearchProfileSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]
   pagination_class = PageNumberPagination

   def get_queryset(self):
      """Get the queryset for the dedicated search view"""
      queryset = Profile.objects.select_related(
         'user').prefetch_related('tags').all()

      # Get search parameters
      search_query = self.request.query_params.get('q', '')
      user_type = self.request.query_params.get('user_type', '')
      location = self.request.query_params.get('location', '')
      city = self.request.query_params.get('city', '')
      tags = self.request.query_params.getlist('tags', [])

      # Apply filters
      if search_query:
         queryset = apply_filters(search_query, queryset)

      if user_type:
         queryset = queryset.filter(user_type=user_type)

      if location:
         queryset = queryset.filter(
         Q(city__icontains=location) |
         Q(state__icontains=location) |
         Q(country__icontains=location)
         )

      if city:
         queryset = queryset.filter(city__icontains=city)

      if tags:
         tag_objects = Tag.objects.filter(tag_name__in=tags)
         if tag_objects.exists():
            for tag in tag_objects:
               queryset = queryset.filter(tags=tag)
            queryset = queryset.distinct()

      return queryset

def apply_filters(search_query, queryset):
   search_terms = search_query.split()
   name_filters = []
   for term in search_terms:
      name_filters.append(
         Q(first_name__icontains=term) |
         Q(last_name__icontains=term)
      )
   if name_filters:
      queryset = queryset.filter(reduce(operator.and_, name_filters))

   return queryset
