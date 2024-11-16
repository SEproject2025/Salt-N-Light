from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django.contrib.auth import login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User, Supporter, Missionary,\
                    Tag, TagRecord, SearchHistory,\
                    ExternalMedia
from .serializer import UserSerializer, SupporterSerializer,\
                        MissionarySerializer, TagSerializer,\
                        TagRecordSerializer, SeachHistorySerializer,\
                        ExternalMediaSerializer, LoginSerializer,\
                        RegistrationSerializer, UserDetailSerializer

# User viewset that performs CRUD operations
class UserViewSet(ModelViewSet):
   filterset_fields = ['user_type','description','phone_number']
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [AllowAny]

# Supporter viewset that performs CRUD operations
class SupporterViewSet(ModelViewSet):
   filterset_fields = ['name','denomination','street_address','city',
                       'state','country']
   queryset = Supporter.objects.all()
   serializer_class = SupporterSerializer
   permission_classes = [IsAuthenticated]

# Missionary viewset performs CRUD operations
class MissionaryViewSet(ModelViewSet):
   filterset_fields = ['full_name','denomination','country',
                       'years_of_experience']
   queryset = Missionary.objects.all()
   serializer_class = MissionarySerializer
   permission_classes = [IsAuthenticated]

# Tag viewset that performs CRUD operations
class TagViewSet(ModelViewSet):
   filterset_fields = ['tag_name','tag_description','tag_is_predefined']
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [IsAuthenticated]

# Tag record viewset that performs CRUD operations
class TagRecordViewSet(ModelViewSet):
   filterset_fields = ['tag','user','added_date']
   queryset = TagRecord.objects.all()
   serializer_class = TagRecordSerializer
   permission_classes = [IsAuthenticated]

# Search history viewset that performs CRUD operations
class SearchHistoryViewSet(ModelViewSet):
   queryset = SearchHistory.objects.all()
   serializer_class = SeachHistorySerializer
   permission_classes = [IsAuthenticated]

# External media viewset that performs CRUD operations
class ExternalMediaViewSet(ModelViewSet):
   queryset = ExternalMedia.objects.all()
   serializer_class = ExternalMediaSerializer
   permission_classes = [IsAuthenticated]

# API view for validating user login
@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
   serializer_class = LoginSerializer
   permission_classes = [AllowAny]
   authentication_classes = [SessionAuthentication]

   # Logs user in and creates a session
   def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
         user = serializer.validated_data
         login(request, user)
         return Response({'message':'login successful'},
                         status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout API view
class LogoutView(APIView):
   permission_classes = [IsAuthenticated]
   def post(self, request):
      logout(request)
      return Response({'message':'logout successful'},
                      status=status.HTTP_200_OK)

# User registration/creation view
@method_decorator(ensure_csrf_cookie, name='dispatch')
class RegistrationView(APIView):
   serializer_class = RegistrationSerializer
   permission_classes = [AllowAny]
   authentication_classes = [SessionAuthentication]

   # Handles user registration
   def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({'message':'account created successfully'},
                         status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API View for retrieving user details (user type, associated tags)
User = get_user_model()
class UserDetailView(APIView):
   permission_classes = [IsAuthenticated]

   # Retrieves a specific user by thier user ID
   def get(self, _request, pk):
      try:
         user = User.objects.get(pk=pk)
         serializer = UserDetailSerializer(user)
         return Response(serializer.data, status=status.HTTP_200_OK)
      except User.DoesNotExist:
         return Response({'message':'user not found'},
                         status=status.HTTP_404_NOT_FOUND)
