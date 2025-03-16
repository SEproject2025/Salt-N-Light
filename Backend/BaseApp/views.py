from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters, views, response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Tag, SearchHistory,\
                    ExternalMedia, Profile, ProfileVote, ProfileComment, ProfileTagging
from .serializer import TagSerializer, SearchHistorySerializer,\
                        ExternalMediaSerializer,\
                        ProfileSerializer, ProfileVoteSerializer, ProfileCommentSerializer

from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.decorators import action

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
   permission_classes = [AllowAny]  # Allow public access

   def get_permissions(self):
      if self.action in ['create', 'update', 'partial_update', 'destroy']:
         return [IsAuthenticated()]
      return [AllowAny()]

   @action(detail=False, methods=['post'], url_path='add-to-profile', url_name='add_to_profile')
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

         # Create the ProfileTagging instance
         ProfileTagging.objects.create(
            profile=profile,
            tag=tag,
            added_by=request.user,
            is_self_added=(request.user.id == profile.user.id)
         )

         return Response({
            'message': f'Tag "{tag.tag_name}" added to profile successfully',
            'tag_id': tag.id,
            'profile_id': profile_id
         }, status=status.HTTP_200_OK)

      except Profile.DoesNotExist:
         return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
         )
      except Tag.DoesNotExist:
         return Response(
            {'error': 'Tag not found'}, 
            status=status.HTTP_404_NOT_FOUND
         )
      except Exception as e:
         return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
         )

   @action(detail=False, methods=['post'], url_path='remove-from-profile', url_name='remove_from_profile')
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

         # Delete the ProfileTagging instance
         tagging = ProfileTagging.objects.filter(
            profile=profile,
            tag=tag,
            added_by=request.user
         ).first()

         if not tagging:
            return Response(
               {'error': 'Tag not found or you do not have permission to remove it'}, 
               status=status.HTTP_404_NOT_FOUND
            )

         tagging.delete()

         return Response({
            'message': f'Tag "{tag.tag_name}" removed from profile successfully',
            'tag_id': tag.id,
            'profile_id': profile_id
         }, status=status.HTTP_200_OK)

      except Profile.DoesNotExist:
         return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
         )
      except Tag.DoesNotExist:
         return Response(
            {'error': 'Tag not found'}, 
            status=status.HTTP_404_NOT_FOUND
         )
      except Exception as e:
         return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
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
