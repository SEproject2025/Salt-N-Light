from django.urls import path, include
from rest_framework import routers

# Imports all views from view.py
from .views import matching, authView, ChurchViewSet

router = routers.DefaultRouter()
router.register('church', ChurchViewSet)

urlpatterns = [
   path('routers/', include(router.urls)),
   path('matching/', matching, name='matching'),
   path('', authView, name ="authView"),
   path('accounts/', include("django.contrib.auth.urls")),
]
