import os
import sys
import django

# Get the absolute path of the project root (Salt-N-Light)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to sys.path
sys.path.append(project_root)

# Set the Django settings module using correct case
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

# Set up Django
django.setup()

import requests
from django.contrib.auth.models import User
from BaseApp.models import Profile

def test_search():
    # Get a test user's token
    user = User.objects.get(username='testuser1')
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # Test search endpoint
    base_url = 'http://localhost:8000'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Test cases
    test_cases = [
        {'name': 'Empty search', 'params': {}},
        {'name': 'Search by type (missionary)', 'params': {'user_type': 'missionary'}},
        {'name': 'Search by type (church)', 'params': {'user_type': 'church'}},
        {'name': 'Search by location (Tokyo)', 'params': {'location': 'Tokyo'}},
        {'name': 'Search by name (David)', 'params': {'q': 'David'}},
        {'name': 'Search with page_size=all', 'params': {'page_size': 'all'}}
    ]
    
    print("\nTesting search endpoint...")
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        response = requests.get(
            f'{base_url}/api/profiles/search/',
            headers=headers,
            params=test['params']
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {len(data.get('results', []))} profiles found")
            if data.get('results'):
                print("First profile:")
                profile = data['results'][0]
                print(f"  Name: {profile.get('first_name')} {profile.get('last_name')}")
                print(f"  Type: {profile.get('user_type')}")
                print(f"  Location: {profile.get('city')}, {profile.get('country')}")
        else:
            print(f"Error: {response.text}")

if __name__ == '__main__':
    test_search() 