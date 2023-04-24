from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.urls import path
from rest_framework import generics
from .views import PasswordResetView, PasswordResetConfirmView

router = routers.SimpleRouter()
router.register(r'player', views.PlayerViewSet)
router.register(r'friend', views.FriendViewSet)
router.register(r'party', views.PartyViewSet)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
    path('playerName/<str:username>/', views.PlayerFindWithUsername),
    path('addParticipant/<int:player>/<int:party>/', views.AddParticipant)
]
urlpatterns += router.urls
