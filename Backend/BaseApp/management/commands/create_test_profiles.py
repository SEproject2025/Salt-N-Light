"""Management command to create test profiles for development and testing."""

import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from BaseApp.models import Profile, Tag

# Configure logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
   """Django command to create test profiles."""
   
   help = 'Creates test profiles for development and testing'

   def __init__(self):
      """Initialize command with test data."""
      super().__init__()
      self.test_profiles = [
         {
            'username': 'testcypressuser1',
            'password': 'TestPass123!',
            'email': 'test1@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'profile': {
               'user_type': 'missionary',
               'is_anonymous': False,
               'city': 'Tokyo',
               'state': 'Tokyo',
               'country': 'Japan',
               'description': 'Test missionary in Tokyo',
               'tags': ['Teaching', 'Youth Ministry']
            }
         },
         {
            'username': 'testsupporter1',
            'password': 'SupportPass123!',
            'email': 'supporter1@example.com',
            'first_name': 'First',
            'last_name': 'Supporter',
            'profile': {
               'user_type': 'supporter',
               'is_anonymous': False,
               'city': 'Seoul',
               'state': 'Seoul',
               'country': 'South Korea',
               'description': 'Test supporter in Seoul',
               'tags': ['Prayer Support', 'Financial Support']
            }
         },
         {
            'username': 'testmissionary1',
            'password': 'MissionPass123!',
            'email': 'missionary1@example.com',
            'first_name': 'David',
            'last_name': 'Kim',
            'profile': {
               'user_type': 'missionary',
               'is_anonymous': False,
               'city': 'Bangkok',
               'state': 'Bangkok',
               'country': 'Thailand',
               'description': 'Test missionary in Bangkok',
               'tags': ['Church Planting', 'Evangelism']
            }
         },
         {
            'username': 'testanonymous1',
            'password': 'AnonPass123!',
            'email': 'anon1@example.com',
            'first_name': '',
            'last_name': '',
            'profile': {
               'user_type': None,
               'is_anonymous': True,
               'city': '',
               'state': '',
               'country': '',
               'description': '',
               'tags': []
            }
         }
      ]

   def _create_tags(self, tag_names):
      """Create tags if they don't exist and return tag objects.
      
      Args:
         tag_names (list): List of tag names to create
         
      Returns:
         list: List of Tag objects
      """
      tags = []
      for tag_name in tag_names:
         tag, _ = Tag.objects.get_or_create(tag_name=tag_name)
         tags.append(tag)
      return tags

   def _create_user_and_profile(self, user_data):
      """Create a user and associated profile.
      
      Args:
         user_data (dict): Dictionary containing user and profile data
         
      Returns:
         tuple: Created User and Profile objects
      """
      # Create user
      user = User.objects.create_user(
         username=user_data['username'],
         email=user_data['email'],
         password=user_data['password'],
         first_name=user_data['first_name'],
         last_name=user_data['last_name']
      )

      # Create profile
      profile_data = user_data['profile']
      profile = Profile.objects.create(
         user=user,
         user_type=profile_data['user_type'],
         is_anonymous=profile_data['is_anonymous'],
         city=profile_data['city'],
         state=profile_data['state'],
         country=profile_data['country'],
         description=profile_data['description']
      )

      # Add tags
      tags = self._create_tags(profile_data['tags'])
      profile.tags.add(*tags)

      return user, profile

   def handle(self, *args, **options):
      """Execute the command to create test profiles."""
      try:
         with transaction.atomic():
            for profile_data in self.test_profiles:
               # Skip if user already exists
               if User.objects.filter(username=profile_data['username']).exists():
                  self.stdout.write(
                     self.style.WARNING(
                        f"User {profile_data['username']} already exists, skipping..."
                     )
                  )
                  continue

               user, profile = self._create_user_and_profile(profile_data)
               self.stdout.write(
                  self.style.SUCCESS(
                     f"Created user and profile for {user.username}"
                  )
               )

         self.stdout.write(
            self.style.SUCCESS("Successfully created all test profiles")
         )

      except Exception as e:
         logger.error("Error creating test profiles: %s", str(e))
         self.stdout.write(
            self.style.ERROR(f"Failed to create test profiles: {str(e)}")
         ) 