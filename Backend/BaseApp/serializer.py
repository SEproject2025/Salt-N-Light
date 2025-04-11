from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment, Notification


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
      extra_kwargs = {
         'password': {'write_only': True},
         'id': {'read_only': True}
      }

   def create(self, validated_data):
      return User.objects.create_user(**validated_data)

# Serializer class for Tags
class TagSerializer(serializers.ModelSerializer):
   is_self_added = serializers.SerializerMethodField()

   class Meta:
      model = Tag
      fields = ['id', 'tag_name', 'tag_description',
      'tag_is_predefined', 'is_self_added']

   def get_is_self_added(self, obj):
      request = self.context.get('request')
      profile_id = self.context.get('profile_id')
      if not request or not profile_id:
         return False
      try:
         tagging = obj.profiletagging_set.filter(
            profile_id=profile_id
         ).first()
         return tagging.is_self_added if tagging else False
      except ObjectDoesNotExist:
         return False

# Simple serializer that only returns tag IDs
class TagIdSerializer(serializers.ModelSerializer):
   class Meta:
      model = Tag
      fields = ['id']

class ProfileVoteSerializer(serializers.ModelSerializer):
   voter_username = serializers.CharField(
      source='voter.username', read_only=True)

   class Meta:
      model = ProfileVote
      fields = ['id', 'voter', 'voter_username', 'profile',
                'is_upvote', 'created_at', 'updated_at']
      read_only_fields = ['voter', 'created_at', 'updated_at']

   def create(self, validated_data):
      # Set the voter to the current user
      validated_data['voter'] = self.context['request'].user
      return super().create(validated_data)


class ProfileCommentSerializer(serializers.ModelSerializer):
   commenter_username = serializers.CharField(
      source='commenter.username', read_only=True)

   class Meta:
      model = ProfileComment
      fields = ['id', 'commenter', 'commenter_username',
                'profile', 'comment', 'created_at', 'updated_at']
      read_only_fields = ['commenter', 'created_at', 'updated_at']

   def create(self, validated_data):
      # Set the commenter to the current user
      validated_data['commenter'] = self.context['request'].user
      return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
   user = UserSerializer(read_only=True)
   tags = serializers.PrimaryKeyRelatedField(
      queryset=Tag.objects.all(),
      many=True,
      required=False,
      allow_empty=True
   )
   description = serializers.CharField(required=False, allow_blank=True)

   class Meta:
      model = Profile
      fields = ['id', 'user', 'tags', 'description']

   def to_representation(self, instance):
      data = super().to_representation(instance)
      # Convert tag IDs to full tag objects if enriched=true
      if self.context.get('request') and self.context['request'].query_params.get('enriched') == 'true':
         data['tags'] = TagSerializer(instance.tags.all(), many=True).data
      return data

class ProfileEnrichedSerializer(ProfileSerializer):
   tags = TagSerializer(many=True, read_only=True)
   current_user_vote = serializers.SerializerMethodField()
   vote_count = serializers.SerializerMethodField()

   class Meta(ProfileSerializer.Meta):
      fields = ProfileSerializer.Meta.fields + ['current_user_vote', 'vote_count']

   def get_current_user_vote(self, obj):
      request = self.context.get('request')
      if request and request.user.is_authenticated:
         vote = ProfileVote.objects.filter(
            profile=obj,
            voter=request.user
         ).first()
         return vote.is_upvote if vote else None
      return None

   def get_vote_count(self, obj):
      return obj.votes_received.count()

# Serializer class for Search History
class SearchHistorySerializer(serializers.ModelSerializer):
   class Meta:
      model = SearchHistory
      fields = '__all__'

# Serializer class for External Media
class ExternalMediaSerializer(serializers.ModelSerializer):
   class Meta:
      model = ExternalMedia
      fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
   recipient_username = serializers.CharField(
      source='recipient.username', read_only=True)
   created_at = serializers.DateTimeField(
      format="%Y-%m-%d %H:%M:%S", read_only=True)

   class Meta:
      model = Notification
      fields = '__all__'
      read_only_fields = ['created_at']
