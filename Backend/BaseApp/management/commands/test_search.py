from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import requests

class Command(BaseCommand):
    help = 'Test the search endpoint functionality'

    def handle(self, *args, **options):
        # Get a test user's token
        user = User.objects.get(username='testuser1')
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
        
        self.stdout.write("\nTesting search endpoint...")
        for test in test_cases:
            self.stdout.write(f"\nTest: {test['name']}")
            response = requests.get(
                f'{base_url}/api/profiles/search/',
                headers=headers,
                params=test['params']
            )
            
            self.stdout.write(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                self.stdout.write(f"Results: {len(data.get('results', []))} profiles found")
                if data.get('results'):
                    self.stdout.write("First profile:")
                    profile = data['results'][0]
                    self.stdout.write(f"  Name: {profile.get('first_name')} {profile.get('last_name')}")
                    self.stdout.write(f"  Type: {profile.get('user_type')}")
                    self.stdout.write(f"  Location: {profile.get('city')}, {profile.get('country')}")
            else:
                self.stdout.write(f"Error: {response.text}") 