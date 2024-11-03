from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from .views import matching, authView, ChurchViewSet, MissionaryViewSet, church_post

#Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('church', ChurchViewSet)
router.register('missionary', MissionaryViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('matching/', matching, name='matching'),
   path('auth/', authView, name ="authView"),
   path('accounts/', include("django.contrib.auth.urls")),
   path('churchpost/', church_post, name = "church_post" ),
]
