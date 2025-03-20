from django.contrib import admin

# Register your models here.
from .models import Tag, SearchHistory, ExternalMedia, Notification

# Registering tables into admin/
admin.site.register(Tag)
admin.site.register(SearchHistory)
admin.site.register(ExternalMedia)
admin.site.register(Notification)
