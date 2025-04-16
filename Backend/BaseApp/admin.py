from django.contrib import admin

# Register your models here.
from .models import Tag, SearchHistory, ExternalMedia, Notification, \
                    ProfileVote, ProfileTagging, ProfileComment, \
                    Friendship

# Registering tables into admin/
admin.site.register(Tag)
admin.site.register(SearchHistory)
admin.site.register(ExternalMedia)
admin.site.register(Notification)
admin.site.register(ProfileVote)
admin.site.register(ProfileTagging)
admin.site.register(ProfileComment)
admin.site.register(Friendship)