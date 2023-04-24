from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.SimpleRouter()
router.register(r'player', views.PlayerViewSet)
router.register(r'friend', views.FriendViewSet)
router.register(r'party', views.PartyViewSet)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('playerName/<str:username>/', views.PlayerFindWithUsername),
    path('addParticipant/<int:player>/<int:party>/', views.AddParticipant),
    path('accept/<int:participant_id>/', views.accept_invitation),
    path('addfirend/<int:player1_id>/<int:player2_id>/', views.add_friend),
    path('acceptfriend/<int:friend_id>/', views.accept_friendship),
]
urlpatterns += router.urls
