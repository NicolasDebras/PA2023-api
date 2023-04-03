from django.urls import path
from . import views

urlpatterns = [
    path('player/', views.AllPlayerGet),
    path('player/<int:id>/', views.PlayerGet)
]
    