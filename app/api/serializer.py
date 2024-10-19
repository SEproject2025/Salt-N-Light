from rest_framework import serializers
from .models        import Missionary, Church

#Serializer class for missionaries
class MissionarySerializer(serializers.ModelSerializer):
   class Meta:
      model  = Missionary
      fields = ('id', 'missionary_name', 'email_address', 'phone_number', 'field_of_service')

#Serializer class for churhes
class ChurchSerializer(serializers.ModelSerializer):
   class Meta:
      model  = Church
      fields = ('id', 'church_name', 'pastor_name', 'church_address', 'church_number', 'email_address')



   