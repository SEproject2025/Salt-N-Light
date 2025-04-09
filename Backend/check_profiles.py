import os
import django
import sys

# Get the absolute path of the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to Python path
sys.path.append(current_dir)

# Set up Django environment with the correct module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saltnlight.settings')
django.setup()

from BaseApp.models import Profile, Tag, ProfileTagging
from django.contrib.auth.models import User

def check_profiles():
    print("\nChecking database contents...")
    
    # Check total number of profiles
    total_profiles = Profile.objects.count()
    print(f"\nTotal profiles in database: {total_profiles}")
    
    # Check profiles with tags
    profiles_with_tags = Profile.objects.filter(tags__isnull=False).distinct().count()
    print(f"Profiles with tags: {profiles_with_tags}")
    
    # Check profiles without tags
    profiles_without_tags = Profile.objects.filter(tags__isnull=True).count()
    print(f"Profiles without tags: {profiles_without_tags}")
    
    # List all users and their profiles
    print("\nListing all users and their profiles:")
    for user in User.objects.all():
        try:
            profile = Profile.objects.get(user=user)
            tag_count = profile.tags.count()
            print(f"\nUsername: {user.username}")
            print(f"Name: {user.first_name} {user.last_name}")
            print(f"User Type: {profile.user_type}")
            print(f"Location: {profile.city}, {profile.country}")
            print(f"Tags: {tag_count}")
            print(f"Experience: {profile.years_of_experience} years")
        except Profile.DoesNotExist:
            print(f"\nUser {user.username} has no profile")

if __name__ == '__main__':
    check_profiles() 