from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from .views import matching, authView, ChurchViewSet, MissionaryViewSet, account_creation, user_login, user_profile

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('church', ChurchViewSet)
router.register('missionary', MissionaryViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('matching/', matching, name='matching'),
   path('auth/', authView, name ="authView"),
   path('accounts/', include("django.contrib.auth.urls")),
   path('createaccount/', account_creation, name = "account_creation" ),
   path('userlogin/', user_login, name = "user_login"),
   path('userprofile/', user_profile, name = "user_profile"),
]
