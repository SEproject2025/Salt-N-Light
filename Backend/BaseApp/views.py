# Imports
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Missionary, Church
from .serializer import ChurchSerializer, MissionarySerializer

# Gets all church and missionary objects and renders the data on matching.html
@login_required
def matching(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   data = {
       'churches': church_data,
       'missionaries': missionary_data,
   }
   return render(request, 'matching.html', context=data)

@login_required
def home(request):
   return render(request,"matching.html")

def authView(request):
   if request.method =="POST":
      form = UserCreationForm(request.POST or None)
      if form.is_valid():
         form.save()
         return redirect("/accounts/login/")
   else:
      form = UserCreationForm()
   return render(request, "registration/signup.html",{"form": form})

#Basic ViewSet class for churches that can perform all CRUD operations
class ChurchViewSet(ModelViewSet):
   queryset = Church.objects.all()
   serializer_class = ChurchSerializer

#Basic ViewSet class for missionaries that can perform all CRUD operations
class MissionaryViewSet(ModelViewSet):
   queryset = Missionary.objects.all()
   serializer_class = MissionarySerializer

#Mock endpoint that the account creation page uses for reference
@api_view(['POST'])
def account_creation(request):
   if request.method =="POST":
      return JsonResponse({"message": "Request recieved!"}, status=status.HTTP_200_OK)

#Mock endpoint that the login page can use for reference
@api_view(['POST', 'GET'])
def user_login(request):
   if request.method == "POST":
      return JsonResponse({"message": "Request recieved!"}, status=status.HTTP_200_OK)
   if request.method == "GET":
      return JsonResponse({"message": "Request recieved!"}, status=status.HTTP_200_OK)
   
#Mock endpoint that the Profile Page can use for reference
@api_view(['PUT', 'GET', 'POST'])
def user_profile(request):
   if request.method == 'PUT':
      return JsonResponse({"message": "Request recieved!"}, status=status.HTTP_200_OK)
   if request.method == 'POST':
      return JsonResponse({"message": "Request recieved!"}, status=status.HTTP_200_OK)
   if request.method == 'GET':
      return JsonResponse({"message": "Request recieved!"}, status=status.HTTP_200_OK)