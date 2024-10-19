from django.urls import path, include

#Imports all views from view.py
from . import views

urlpatterns = [
   path('missionaries/', views.missionaries, name = 'missionaries'),
   path('churches/', views.churches, name = 'churches'),
   path('users/', views.users, name = 'users'),
   path('connections_list/', views.connections_list, name = 'connections_list'),

   path('login/', views.login, name='login'),
   path('signup/', views.signup, name='signup'),  # Optional for registration
   path('connections/', views.connections_list, name='connections_list'),
   path('logout/', views.logout_view, name='logout'),

]