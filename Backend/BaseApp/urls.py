from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, SearchHistoryViewSet, \
    ExternalMediaViewSet, \
    ProfileListCreateView, ProfileDetailView, \
    MatchmakingResultsView, CurrentUserView, \
    ProfileVoteView, ProfileCommentView, \
    ProfileVoteStatusView, NotificationView, FriendshipViewSet, \
    check_superuser, AdminProfileListView, AdminProfileDeleteView, \
    AdminCommentListView, AdminCommentDeleteView

# Automatically generates URLs for all ViewSet classes
router = routers.DefaultRouter()
router.register('api/notifications', NotificationView, basename='notification')
router.register('friendships', FriendshipViewSet, basename='friendship')
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
   path('api/friendships/<int:pk>/respond/',
        FriendshipViewSet.as_view({'post': 'respond'}),
        name='friendship-respond'),
   path('api/friendships/', FriendshipViewSet.as_view({'post': 'create'}),
        name='friendship-create'),
   path('api/friendships/status/<int:profile_id>/',
        FriendshipViewSet.as_view({'get': 'status'}),
        name='friendship-status'),

   # Admin API endpoints
   path('api/admin/check-superuser/', check_superuser,
        name='admin-check-superuser'),
   path('api/admin/profiles/', AdminProfileListView.as_view(),
        name='admin-profile-list'),
   path('api/admin/profiles/<int:pk>/',
        AdminProfileDeleteView.as_view(), name='admin-profile-delete'),
   path('api/admin/comments/', AdminCommentListView.as_view(),
        name='admin-comment-list'),
   path('api/admin/comments/<int:pk>/',
        AdminCommentDeleteView.as_view(), name='admin-comment-delete'),
]
