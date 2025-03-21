from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from profanity.validators import validate_is_profane

# Defines the Tag table
class Tag(models.Model):
   tag_name = models.CharField(max_length=100, null=False)
   tag_description = models.TextField(blank=True)
   tag_is_predefined = models.BooleanField(default=True)

# Defines the Supporter table
class Profile(models.Model):
   user = models.OneToOneField(
      User,
      on_delete=models.CASCADE, primary_key=True)
   user_type = models.CharField(
       max_length=15,
       choices=[('missionary', 'Missionary'), ('supporter', 'Supporter'),
                ('other', 'Other')],
       default='other', blank=True, null=True
    )
   first_name = models.CharField(max_length=100, blank=True, null=True)
   last_name = models.CharField(max_length=100, blank=True, null=True)
   denomination = models.CharField(max_length=100, blank=True, null=True)
   street_address = models.CharField(max_length=100, blank=True, null=True)
   city = models.CharField(max_length=100, blank=True, null=True)
   state = models.CharField(max_length=100, blank=True, null=True)
   country = models.CharField(max_length=100, blank=True, null=True)
   phone_number = models.CharField(max_length=100, blank=True, null=True)
   years_of_experience = models.IntegerField(blank=True, null=True)
   description = models.TextField(blank=True, null=True)
   profile_picture = models.URLField(max_length=225, null=True, blank=True)

   # Sample tag field
   tags = models.ManyToManyField(Tag, related_name='profiles', blank=True)

   def __str__(self):
      return f"{self.user.username} - {self.user_type}"  # pylint: disable=no-member

# Defines Search History table
class SearchHistory(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   search_time = models.DateTimeField(auto_now_add=True)
   search_text = models.TextField(null=False)
   search_parameters = models.JSONField()

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "Search History"

# Defines External Media table
class ExternalMedia(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   media_url = models.URLField(max_length=255)
   description = models.TextField()
   uploaded_at = models.DateTimeField(auto_now_add=True)

   # Overwrites the automatic plural form of words in admin
   class Meta:
      verbose_name_plural = "External Media"

class ProfileVote(models.Model):
   voter = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='votes_cast')
   profile = models.ForeignKey(
      Profile, on_delete=models.CASCADE, related_name='votes_received')
   is_upvote = models.BooleanField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      # Ensures one vote per user per profile
      unique_together = ('voter', 'profile')

   def clean(self):
      if self.voter == self.profile.user:  # pylint: disable=no-member
         raise ValidationError("Users cannot vote on their own profile")


class ProfileComment(models.Model):
   commenter = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='comments_made')
   profile = models.ForeignKey(
      Profile, on_delete=models.CASCADE, related_name='comments_received')
   comment = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      # Ensures one comment per user per profile
      unique_together = ('commenter', 'profile')

   def clean(self):
      if self.commenter == self.profile.user:  # pylint: disable=no-member
         raise ValidationError("Users cannot comment on their own profile")
      # Check if the user has voted before commenting
      if not ProfileVote.objects.filter(
         voter=self.commenter, profile=self.profile).exists():
         raise ValidationError("Must vote before commenting")

class Notification(models.Model):
   NOTIFICATION_TYPES = [
      ('friend_request', 'Friend Request'),
      ('general', 'General'),
   ]

   recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='notifications')
   notification_type = models.CharField(max_length=20,
                                        choices=NOTIFICATION_TYPES)
   message = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)
   is_read = models.BooleanField(default=False)
   related_object_id = models.IntegerField(null=True, blank=True)

   class Meta:
      ordering = ['-created_at']

   def __str__(self):
      return f"{
         self.notification_type} notification for {self.recipient.username}" # pylint: disable=no-member

# Define profane filter word validator
class Comment(models.Model):
    content = models.TextField(validators=[validate_is_profane])