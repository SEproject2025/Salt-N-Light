from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .test_data import create_test_data
from BaseApp.models import Profile
from django.db.models import Q

class SearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests"""
        create_test_data()
        cls.test_user = User.objects.get(username='testuser1')
        refresh = RefreshToken.for_user(cls.test_user)
        cls.access_token = str(refresh.access_token)

    def setUp(self):
        """Set up the test client with authentication"""
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_empty_search(self):
        """Test search with no parameters"""
        response = self.client.get('/api/search/')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0, 
                          "Empty search should return some results")

    def test_search_by_type_missionary(self):
        """Test searching for missionaries"""
        response = self.client.get('/api/search/?user_type=missionary')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        for result in response.data:
            self.assertEqual(result['user_type'], 'missionary')

    def test_search_by_type_church(self):
        """Test searching for churches"""
        response = self.client.get('/api/search/?user_type=church')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        for result in response.data:
            self.assertEqual(result['user_type'], 'church')

    def test_search_by_location(self):
        """Test searching by location"""
        response = self.client.get('/api/search/?city=Tokyo')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        for result in response.data:
            self.assertEqual(result['city'], 'Tokyo')

    def test_search_by_name(self):
        """Test searching by name with combined name search field"""
        # Test full name search
        response = self.client.get('/api/search/?q=David Kim')
        print("\nFull name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        self.assertGreater(len(results), 0, "Should find profiles with 'David Kim'")
        for result in results:
            user = result['user']
            # Either first name or last name should contain the search terms
            self.assertTrue(
                ('David' in user['first_name'] and 'Kim' in user['last_name']) or
                ('David' in user['last_name'] and 'Kim' in user['first_name']) or
                ('David' in result['description'] and 'Kim' in result['description'])
            )

        # Test partial name search
        response = self.client.get('/api/search/?q=David')
        print("\nPartial name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        self.assertGreater(len(results), 0, "Should find profiles with 'David'")
        for result in results:
            user = result['user']
            # The name should appear in either first name, last name, or description
            self.assertTrue(
                'David' in user['first_name'] or
                'David' in user['last_name'] or
                'David' in result['description']
            )

        # Test case-insensitive search
        response = self.client.get('/api/search/?q=david')
        print("\nCase-insensitive search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        self.assertGreater(len(results), 0, "Should find profiles with 'david' (case-insensitive)")
        
        # Test search with multiple terms in any order
        response = self.client.get('/api/search/?q=Kim David')
        print("\nReverse order name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        self.assertGreater(len(results), 0, "Should find profiles with 'Kim David'")

    def test_search_with_page_size_all(self):
        """Test getting all results"""
        response = self.client.get('/api/search/?page_size=all')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0, 
                          "Should return all profiles")
        self.assertIsNone(response.data.get('next'), 
                         "Should not have pagination with page_size=all")

    def test_search_with_invalid_parameters(self):
        """Test search with invalid parameters"""
        response = self.client.get('/api/search/?invalid_param=value')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200, 
                        "Invalid parameters should be ignored, not cause errors")

    def test_search_without_authentication(self):
        """Test search without authentication"""
        client = APIClient()  # Create new unauthenticated client
        response = client.get('/api/search/')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 401, 
                        "Should require authentication")

    def test_search_with_tags(self):
        """Test searching by tags"""
        response = self.client.get('/api/search/?tags=Missionary')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', [])
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertTrue(any(tag['tag_name'] == 'Missionary' for tag in result['tags']))

    def test_search_with_multiple_tags(self):
        """Test searching with multiple tags"""
        # Debug: Print all profiles and their tags
        all_profiles = Profile.objects.all()
        print("\nAll profiles and their tags:")
        for profile in all_profiles:
            tag_names = [tag.tag_name for tag in profile.tags.all()]
            print(f"Profile (User ID: {profile.user.id}): {tag_names}")
        
        # Use the correct endpoint and tag format
        params = {'tags': ['Missionary', 'Teaching']}
        response = self.client.get('/api/search/', params)
        print("\nResponse content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        self.assertGreater(len(results), 0)
        for result in results:
            tag_names = [tag['tag_name'] for tag in result['tags']]
            print(f"Result tags: {tag_names}")  # Debug print
            self.assertTrue('Missionary' in tag_names or 'Teaching' in tag_names)

    def test_search_with_non_existent_tag(self):
        """Test searching with a non-existent tag"""
        response = self.client.get('/api/search/?tags=NonExistentTag')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_search_with_duplicate_names(self):
        """Test searching for duplicate names using static test data"""
        # Ensure we're using the authenticated client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Test searching for duplicate first names
        response = self.client.get('/api/search/?q=David')
        print("\nDuplicate first name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        # Get all Davids from the static test data
        static_davids = User.objects.filter(first_name='David')
        print(f"\nFound {static_davids.count()} Davids in static test data")
        
        # Compare against static test data
        david_count = sum(1 for result in results 
                         if 'David' in result['user']['first_name'])
        self.assertEqual(david_count, static_davids.count(), 
                        f"Should find exactly {static_davids.count()} Davids from static test data")

        # Test searching for duplicate full names
        response = self.client.get('/api/search/?q=David Kim')
        print("\nDuplicate full name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        # Get all David Kims from the static test data
        static_david_kims = User.objects.filter(first_name='David', last_name='Kim')
        print(f"\nFound {static_david_kims.count()} David Kims in static test data")
        
        # Compare against static test data
        david_kim_count = sum(1 for result in results 
                            if 'David' in result['user']['first_name'] 
                            and 'Kim' in result['user']['last_name'])
        self.assertEqual(david_kim_count, static_david_kims.count(),
                        f"Should find exactly {static_david_kims.count()} David Kims from static test data")

        # Test searching for duplicate last names
        response = self.client.get('/api/search/?q=Kim')
        print("\nDuplicate last name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
            
        # Get all Kims from the static test data
        static_kims = User.objects.filter(last_name='Kim')
        print(f"\nFound {static_kims.count()} Kims in static test data")
        
        # Compare against static test data
        kim_count = sum(1 for result in results 
                       if 'Kim' in result['user']['last_name'])
        self.assertEqual(kim_count, static_kims.count(),
                        f"Should find exactly {static_kims.count()} Kims from static test data")

    def test_search_with_users_without_tags(self):
        """Test searching for users without tags"""
        response = self.client.get('/api/search/')
        print("Response content:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', [])
        users_without_tags = [result for result in results if len(result['tags']) == 0]
        self.assertEqual(len(users_without_tags), 3)  # Should find users 3, 4, and 5

    def test_partial_name_search(self):
        """Test searching with partial names using static test data"""
        # Ensure we're using the authenticated client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Test partial first name search
        response = self.client.get('/api/search/?q=jo')
        print("\nPartial first name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        data = response.data
        # Handle both paginated and non-paginated responses
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
            
        # Get all users with 'jo' in their first or last name from static test data
        static_users_with_jo = User.objects.filter(
            Q(first_name__icontains='jo') | Q(last_name__icontains='jo')
        )
        print(f"\nFound {static_users_with_jo.count()} users with 'jo' in static test data")
        
        # Find matches that contain 'jo' in either first or last name
        matches = [
            result for result in results
            if 'jo' in result['user']['first_name'].lower() or
               'jo' in result['user']['last_name'].lower()
        ]
        print(f"\nFound {len(matches)} matches with 'jo'")  # Debug print
        self.assertEqual(len(matches), static_users_with_jo.count(), 
                        f"Should find exactly {static_users_with_jo.count()} users with 'jo' from static test data")
        
        # Test partial last name search
        response = self.client.get('/api/search/?q=jos')
        print("\nPartial last name search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        data = response.data
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
            
        # Get all users with 'jos' in their last name from static test data
        static_users_with_jos = User.objects.filter(last_name__icontains='jos')
        print(f"\nFound {static_users_with_jos.count()} users with 'jos' in static test data")
        
        # Find matches that contain 'jos' in last name
        matches = [
            result for result in results
            if 'jos' in result['user']['last_name'].lower()
        ]
        print(f"\nFound {len(matches)} Joseph matches")  # Debug print
        self.assertEqual(len(matches), static_users_with_jos.count(),
                        f"Should find exactly {static_users_with_jos.count()} users with 'jos' from static test data")
        
        # Test partial name with multiple words
        response = self.client.get('/api/search/?q=jo doe')
        print("\nMultiple words search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        data = response.data
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
            
        # Get all users with 'jo' in first name and 'doe' in last name from static test data
        static_users_with_jo_doe = User.objects.filter(
            first_name__icontains='jo',
            last_name__icontains='doe'
        )
        print(f"\nFound {static_users_with_jo_doe.count()} users with 'jo' in first name and 'doe' in last name in static test data")
        
        # Find matches that contain 'jo' in first name and 'doe' in last name
        matches = [
            result for result in results
            if 'jo' in result['user']['first_name'].lower() and
               'doe' in result['user']['last_name'].lower()
        ]
        print(f"\nFound {len(matches)} John Doe matches")  # Debug print
        self.assertEqual(len(matches), static_users_with_jo_doe.count(),
                        f"Should find exactly {static_users_with_jo_doe.count()} users with 'jo' in first name and 'doe' in last name from static test data")
        
        # Test case-insensitive partial search
        response = self.client.get('/api/search/?q=JO')
        print("\nCase-insensitive search response:", response.content)  # Debug print
        self.assertEqual(response.status_code, 200)
        data = response.data
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
            
        # Find matches that contain 'jo' in either first or last name (case-insensitive)
        matches = [
            result for result in results
            if 'jo' in result['user']['first_name'].lower() or
               'jo' in result['user']['last_name'].lower()
        ]
        print(f"\nFound {len(matches)} case-insensitive matches")  # Debug print
        self.assertEqual(len(matches), static_users_with_jo.count(),
                        f"Should find exactly {static_users_with_jo.count()} users with 'jo' from static test data") 