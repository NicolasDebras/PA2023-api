from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.urls import path
from rest_framework import generics
from .views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import views as auth_views
router = routers.SimpleRouter()
router.register(r'player', views.PlayerViewSet)
router.register(r'friend', views.FriendViewSet)
router.register(r'party', views.PartyViewSet)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('playerName/<str:username>/', views.PlayerFindWithUsername),
    path('addParticipant/<int:player>/<int:party>/', views.AddParticipant),
    path('accept/<int:participant_id>/', views.accept_invitation),
 #   path('addfirend/<int:player1_id>/<int:player2_id>/', views.add_friend),
 #   path('acceptfriend/<int:friend_id>/', views.accept_friendship),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
      template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
      path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
     path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
urlpatterns += router.urls
