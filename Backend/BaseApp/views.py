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
from .serializer import TagSerializer, TagIdSerializer, SearchHistorySerializer, \
    ExternalMediaSerializer, \
    ProfileSerializer, ProfileVoteSerializer,\
    ProfileCommentSerializer, NotificationSerializer, ProfileEnrichedSerializer

# Set up logging
logger = logging.getLogger(__name__)

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.select_related('user').prefetch_related('tags').all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    search_fields = ['user__username', 'user__email', 'first_name', 'last_name', 'denomination']
    filter_fields = ['user_type', 'city', 'state', 'country', 'denomination']

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.request.query_params.get('enriched') == 'true':
            return ProfileEnrichedSerializer
        return ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.getlist('tags')
        if tags:
            # Handle both tag IDs and tag names
            tag_ids = []
            tag_names = []
            for tag in tags:
                if tag.isdigit():
                    tag_ids.append(int(tag))
                else:
                    tag_names.append(tag)
            
            # Get tag IDs from names
            if tag_names:
                name_tag_ids = Tag.objects.filter(tag_name__in=tag_names).values_list('id', flat=True)
                tag_ids.extend(name_tag_ids)
            
            # Remove duplicates
            tag_ids = list(set(tag_ids))
            
            # Filter profiles that have all the specified tags
            if tag_ids:
                queryset = queryset.filter(tags__in=tag_ids).distinct()
        return queryset


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.select_related('user').prefetch_related('tags').all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.query_params.get('enriched') == 'true':
            return ProfileEnrichedSerializer
        return ProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['profile_id'] = self.kwargs.get('pk')
        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Ensure tags are in the format expected by the frontend
        if 'tags' in data:
            # Each tag should have id, tag_name, and is_self_added
            data['tags'] = [
                {
                    'id': tag['id'],
                    'tag_name': tag['tag_name'],
                    'is_self_added': tag.get('is_self_added', False)
                }
                for tag in data['tags']
            ]

        # Add tag_ids for backward compatibility and frontend editing
        data['tag_ids'] = [tag['id'] for tag in data.get('tags', [])]

        return Response(data)

class MatchmakingResultsView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.query_params.get('enriched') == 'true':
            return ProfileEnrichedSerializer
        return ProfileSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = Profile.objects.exclude(user=self.request.user)
        
        # Add basic matching criteria
        if user_profile.user_type:
            queryset = queryset.filter(user_type=user_profile.user_type)
        if user_profile.country:
            queryset = queryset.filter(country=user_profile.country)
        
        return queryset.select_related('user').prefetch_related('tags')

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

   def get_serializer_class(self):
      if self.action == 'list' and not self.request.query_params.get('full'):
         return TagIdSerializer
      return TagSerializer

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
         profile = Profile.objects.get(id=profile_id)
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
         return Response(
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
   def remove_from_profile(self, request):
      profile_id = request.data.get('profile_id')
      tag_id = request.data.get('tag_id')

      if not profile_id or not tag_id:
         return Response(
            {'error': 'Both profile_id and tag_id are required'},
            status=status.HTTP_400_BAD_REQUEST
         )

      try:
         profile = Profile.objects.get(id=profile_id)
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the user's profile with prefetched tags
            profile = Profile.objects.select_related('user').prefetch_related('tags').get(user=request.user)
            
            # Create context with request and profile_id
            context = {
                'request': request,
                'profile_id': profile.id
            }
            
            # Use enriched serializer by default for display purposes
            serializer = ProfileEnrichedSerializer(profile, context=context)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

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
    queryset = Profile.objects.select_related('user').prefetch_related('tags')
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__user_type', 'user__city', 'user__state', 'user__country', 'user__denomination']
    ordering_fields = ['user__first_name', 'user__last_name', 'user__city', 'user__state']
    ordering = ['user__first_name']

    def get_serializer_class(self):
        if self.request.query_params.get('enriched') == 'true':
            return ProfileEnrichedSerializer
        return ProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_ids = self.request.query_params.getlist('tags')
        tag_names = self.request.query_params.getlist('tag_names')
        
        if tag_ids or tag_names:
            # Convert tag names to IDs if provided
            if tag_names:
                tag_objects = Tag.objects.filter(tag_name__in=tag_names)
                tag_ids.extend([str(tag.id) for tag in tag_objects])
            
            # Remove duplicates and convert to integers
            tag_ids = list(set(map(int, tag_ids)))
            
            # Filter profiles that have ALL the specified tags
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
            
            # Ensure all tags are present (not just any)
            for tag_id in tag_ids:
                queryset = queryset.filter(tags__id=tag_id)
        
        return queryset


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
