from django.shortcuts import render

#My imports 
from .models                 import Missionary, Church
from .serializer             import MissionarySerializer, ChurchSerializer
from django.http             import JsonResponse, HttpResponse
from rest_framework.parsers  import JSONParser
from rest_framework.response import Response
import requests 
#sign up
from django.contrib.auth.forms import UserCreationForm
#user_sign_in imports
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def missionaries(request):
   missionary_data = Missionary.objects.all()
   context = {'missionaries': missionary_data}
   return render(request, 'missionaries.html', context)

def churches(request):
   church_data = Church.objects.all()
   context = {'churches': church_data}
   return render(request, 'churches.html', context)

def users(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   user_data={
      'churches': church_data,
      'missionaries': missionary_data,
   }
   return render(request, 'users.html', user_data)

def connections_list(request):
   church_data = Church.objects.all()
   missionary_data = Missionary.objects.all()

   data={
      'churches': church_data,
      'missionaries': missionary_data,
   }
   return render(request, 'connections_list.html', context = data)

def login(request):
    if request.user.is_authenticated:
        return redirect('connections_list')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('connections_list')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
