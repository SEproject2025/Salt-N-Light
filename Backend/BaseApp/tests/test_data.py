from django.contrib.auth.models import User
from BaseApp.models import Profile, Tag, ProfileTagging
from faker import Faker
import random

def create_test_data():
    """Create test data for search tests"""
    fake = Faker()
    
    # Fixed locations for testing
    locations = [
        {'city': 'Tokyo', 'country': 'Japan'},
        {'city': 'Seoul', 'country': 'South Korea'},
        {'city': 'Manila', 'country': 'Philippines'},
        {'city': 'Bangkok', 'country': 'Thailand'},
        {'city': 'Jakarta', 'country': 'Indonesia'},
        {'city': 'Singapore', 'country': 'Singapore'},
        {'city': 'Kuala Lumpur', 'country': 'Malaysia'},
        {'city': 'Hanoi', 'country': 'Vietnam'},
        {'city': 'Phnom Penh', 'country': 'Cambodia'},
        {'city': 'Vientiane', 'country': 'Laos'}
    ]
    
    # Create test tags
    tags_data = [
        {'tag_name': 'Missionary', 'tag_description': 'Missionary work'},
        {'tag_name': 'Teaching', 'tag_description': 'Teaching ministry'},
        {'tag_name': 'Church Planting', 'tag_description': 'Church planting ministry'},
        {'tag_name': 'Youth Ministry', 'tag_description': 'Youth ministry work'},
        {'tag_name': 'Evangelism', 'tag_description': 'Evangelism ministry'},
        {'tag_name': 'Discipleship', 'tag_description': 'Discipleship ministry'},
        {'tag_name': 'Worship', 'tag_description': 'Worship ministry'},
        {'tag_name': 'Prayer', 'tag_description': 'Prayer ministry'}
    ]
    
    # Create tags
    tags = []
    for tag_data in tags_data:
        tag, created = Tag.objects.get_or_create(
            tag_name=tag_data['tag_name'],
            defaults={'tag_description': tag_data['tag_description']}
        )
        tags.append(tag)
    
    # Create base test users (testuser1 and testuser2)
    base_users_data = [
        {
            'username': 'testuser1',
            'email': 'test1@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile': {
                'user_type': 'missionary',
                'city': 'Tokyo',
                'country': 'Japan',
                'description': 'Test missionary profile',
                'years_of_experience': 5
            }
        },
        {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'testpass123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'profile': {
                'user_type': 'church',
                'city': 'Seoul',
                'country': 'South Korea',
                'description': 'Test church profile',
                'years_of_experience': 10
            }
        }
    ]
    
    # Create base users
    for user_data in base_users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
        
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults=user_data['profile']
        )
        
        # Add all tags to base users
        for tag in tags:
            ProfileTagging.objects.get_or_create(
                profile=profile,
                tag=tag,
                added_by=user,
                is_self_added=True
            )
    
    # Create 20 additional users with random data
    for i in range(3, 23):  # user3 to user22
        first_name = fake.first_name()
        last_name = fake.last_name()
        location = random.choice(locations)
        user_type = random.choice(['missionary', 'church'])
        
        user_data = {
            'username': f'user{i}',
            'email': f'user{i}@example.com',
            'password': 'testpass123',
            'first_name': first_name,
            'last_name': last_name,
            'profile': {
                'user_type': user_type,
                'city': location['city'],
                'country': location['country'],
                'description': fake.sentence(nb_words=6),
                'years_of_experience': random.randint(1, 20)
            }
        }
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
        
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults=user_data['profile']
        )
        
        # Edge case: Some users with no tags
        if i not in [3, 4, 5]:  # users 3, 4, and 5 will have no tags
            # Randomly select 1-4 tags for each user
            num_tags = random.randint(1, 4)
            selected_tags = random.sample(tags, num_tags)
            
            for tag in selected_tags:
                ProfileTagging.objects.get_or_create(
                    profile=profile,
                    tag=tag,
                    added_by=user,
                    is_self_added=True
                )
    
    # Create duplicate name edge cases
    duplicate_names = [
        {'first_name': 'David', 'last_name': 'Kim'},
        {'first_name': 'Sarah', 'last_name': 'Park'}
    ]
    
    for name in duplicate_names:
        for i in range(2):  # Create 2 users with each duplicate name
            location = random.choice(locations)
            user_type = random.choice(['missionary', 'church'])
            
            user_data = {
                'username': f'duplicate_{name["first_name"].lower()}_{i+1}',
                'email': f'duplicate_{name["first_name"].lower()}_{i+1}@example.com',
                'password': 'testpass123',
                'first_name': name['first_name'],
                'last_name': name['last_name']
            }
            
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
            
            profile_data = {
                'user_type': user_type,
                'city': location['city'],
                'country': location['country'],
                'description': fake.sentence(nb_words=6),
                'years_of_experience': random.randint(1, 20)
            }
            
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults=profile_data
            )
            
            # Add random tags to duplicate name profiles
            num_tags = random.randint(1, 4)
            selected_tags = random.sample(tags, num_tags)
            
            for tag in selected_tags:
                ProfileTagging.objects.get_or_create(
                    profile=profile,
                    tag=tag,
                    added_by=user,
                    is_self_added=True
                ) 