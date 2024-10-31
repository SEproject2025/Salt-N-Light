# Imports
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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

class ChurchViewSet(ModelViewSet):
   queryset = Church.objects.all()
   serializer_class = ChurchSerializer

class MissionaryViewSet(ModelViewSet):
   queryset = Missionary.objects.all()
   serializer_class = MissionarySerializer
