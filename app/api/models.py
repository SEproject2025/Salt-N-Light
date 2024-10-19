from django.db import models

# User Models
class Missionary(models.Model):
   missionary_name  = models.CharField(max_length = 100)
   email_address    = models.CharField(max_length = 100)
   phone_number     = models.IntegerField()
   field_of_service = models.CharField(max_length = 100)

   class Meta:
      verbose_name_plural = "Missionaries"

   def __str__(self):
      return self.missionary_name

class Church(models.Model):
   church_name    = models.CharField(max_length = 100)
   church_address = models.CharField(max_length = 100)
   pastor_name    = models.CharField(max_length = 100)
   church_number  = models.IntegerField()
   email_address  = models.CharField(max_length = 100)

   class Meta: 
      verbose_name_plural = "Churches"

   def __str__(self):
      return self.church_name