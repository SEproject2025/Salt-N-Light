from django.urls import path, include

# Imports all views from view.py
from . import views


urlpatterns = [
   path('matching/', views.matching, name='matching'),
   path("signup/", views.authView, name ="authView"),
   path("accounts/", include("django.contrib.auth.urls")),
]
