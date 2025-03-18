from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, SearchHistoryViewSet, \
    ExternalMediaViewSet, \
    ProfileListCreateView, ProfileDetailView, \
    MatchmakingResultsView, CurrentUserView, \
    ProfileVoteView, ProfileCommentView, \
    ProfileVoteStatusView, NotificationView, \
    ProfileSearchView

# Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('api/notifications', NotificationView, basename='notification')
router.register('tag', TagViewSet)
router.register('searchhistory', SearchHistoryViewSet)
router.register('externalmedia', ExternalMediaViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('api/profiles/', ProfileListCreateView.as_view(),
        name='profile-list-create'),
   path('api/profiles/<int:pk>/', ProfileDetailView.as_view(),
        name='profile-detail'),
   path('api/profiles/match', MatchmakingResultsView.as_view()),
   path('api/profiles/me/', CurrentUserView.as_view(),
        name='current-user'),
   path('api/profiles/vote/', ProfileVoteView.as_view(),
        name='profile-vote'),
   path('api/profiles/comment/', ProfileCommentView.as_view(),
        name='profile-comment'),
   path('api/profiles/comment/<int:pk>/',
        ProfileCommentView.as_view(), name='profile-comment-detail'),
   path('api/profiles/<int:profile_id>/vote-status/',
        ProfileVoteStatusView.as_view(),
        name='profile-vote-status'),
   path('api/profiles/search/', ProfileSearchView.as_view(),
        name='profile-search'),
]
