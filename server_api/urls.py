from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.urls import path
from rest_framework import generics

router = routers.SimpleRouter()
router.register(r'player', views.PlayerViewSet)
router.register(r'friend', views.FriendViewSet)
router.register(r'party', views.PartyViewSet)

urlpatterns = [
    path('auth/', views.CustomAuthToken.as_view()),
    path('playerName/<str:username>/', views.PlayerFindWithUsername),
    path('addParticipant/<int:player>/<int:party>/', views.AddParticipant),
    path('accept/<int:participant_id>/', views.accept_invitation),
    path('addfriend/<int:player1_id>/<int:player2_id>/', views.add_friend),
    path('acceptfriend/<int:friend_id>/', views.accept_friendship),
    path('partyfilter/<int:user_id>/', views.patybyuser),
    path('myparty/<int:id_player>/', views.MyPartyView.as_view()),
    path('message/<int:party_id>/', views.MessageByUser)
]
urlpatterns += router.urls
