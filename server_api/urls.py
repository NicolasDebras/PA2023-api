from django.urls import path
from . import views

urlpatterns = [
    path('player/', views.AllPlayerGet),
    path('player/<int:id>/', views.PlayerGet),
    path('addplayer/', views.PlayerAdd),
    path('updateplayer/<int:id>/', views.PlayerUpdate),
    path('deleteplayer/<int:id>/', views.PlayerDelete)
]
    