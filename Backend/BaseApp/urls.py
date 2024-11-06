from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from . import views

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('church', views.ChurchViewSet)
router.register('missionary', views.MissionaryViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('matching/', views.matching, name='matching'),
   path('auth/', views.authView, name ="authView"),
   path('accounts/', include("django.contrib.auth.urls")),
   path('createaccount/', views.account_creation, name = "account_creation" ),
   path('userlogin/', views.user_login, name = "user_login"),
   path('userprofile/', views.user_profile, name = "user_profile"),
]
