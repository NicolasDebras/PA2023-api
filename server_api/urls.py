from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.SimpleRouter()
router.register(r'player', views.PlayerViewSet)
router.register(r'friend', views.FriendViewSet)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('playerName/<str:username>/', views.PlayerFindWithUsername)
]
urlpatterns += router.urls
