from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tag, SearchHistory, \
    ExternalMedia, Profile, ProfileVote, ProfileComment


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
   class Meta:
      model = Tag
      fields = '__all__'


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
