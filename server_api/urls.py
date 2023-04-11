from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.SimpleRouter()
router.register(r'player', views.PlayerViewSet)

urlpatterns = [
    path('auth/', obtain_auth_token),
]
urlpatterns += router.urls
