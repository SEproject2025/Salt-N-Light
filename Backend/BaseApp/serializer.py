from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment, \
    Notification, Friendship


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'password']
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
      tagging = obj.profiletagging_set.filter(
         profile_id=profile_id
               ).first()
      return tagging.is_self_added if tagging else False

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
   user = UserSerializer()  # Nested User serializer
   tags = serializers.PrimaryKeyRelatedField(
       queryset=Tag.objects.all(), many=True, required=False)
   vote_count = serializers.SerializerMethodField()
   comments = ProfileCommentSerializer(
      source='comments_received', many=True, read_only=True)
   current_user_vote = serializers.SerializerMethodField()

   class Meta:
      model = Profile
      fields = '__all__'

   def create(self, validated_data):
      user_data = validated_data.pop('user')
      tag_data = validated_data.pop('tags', [])
      user = User.objects.create_user(**user_data)
      profile = Profile.objects.create(user=user, **validated_data)
      profile.tags.set(tag_data)
      return profile

   def update(self, instance, validated_data):
      user_data = validated_data.pop('user', None)
      tag_data = validated_data.pop('tags', None)

      # Update user fields if provided
      if user_data:
         user_instance = instance.user
         for key, value in user_data.items():
            if key != 'password':  # Don't update password through this method
               setattr(user_instance, key, value)
         user_instance.save()

      # Update all profile fields
      for key, value in validated_data.items():
         if hasattr(instance, key):  # Only set if the field exists
            setattr(instance, key, value)
      instance.save()

      # Update tags if provided
      if tag_data is not None:
         instance.tags.set(tag_data)

      return instance

   def get_vote_count(self, obj):
      upvotes = obj.votes_received.filter(is_upvote=True).count()
      downvotes = obj.votes_received.filter(is_upvote=False).count()
      return upvotes - downvotes

   def get_current_user_vote(self, obj):
      request = self.context.get('request')
      if request and request.user.is_authenticated:
         vote = obj.votes_received.filter(voter=request.user).first()
         if vote:
            return vote.is_upvote
      return None

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
   recipient_username = serializers.CharField(source='recipient.username',
                                              read_only=True)
   created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                          read_only=True)
   class Meta:
      model = Notification
      fields = ['id', 'recipient', 'recipient_username', 'notification_type',
                'message', 'created_at', 'is_read', 'related_object_id']
      read_only_fields = ['created_at']

class FriendshipSerializer(serializers.ModelSerializer):
   sender_username = serializers.CharField(source='sender.username',
                                            read_only=True)
   receiver_username = serializers.CharField(source='receiver.username',
                                              read_only=True)
   class Meta:
      model = Friendship
      fields = ['id', 'sender', 'receiver',
                'status', 'created_at', 'sender_username', 'receiver_username']
      read_only_fields = ['id', 'created_at',
                          'sender_username', 'receiver_username', 'sender']

   def create(self, validated_data):
      # Automatically set the sender to the current user
      validated_data['sender'] = self.context['request'].user
      return super().create(validated_data)
