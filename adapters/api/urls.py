from django.urls import path, include
from . import user_views, player_views, team_views, training_views, tournament_views

app_name = 'api'

urlpatterns = [
    # Users
    path('users/', user_views.user_list, name='user_list'),
    path('users/<int:pk>/', user_views.user_detail, name='user_detail'),
    
    # Players
    path('players/', player_views.player_list, name='player_list'),
    path('players/<int:pk>/', player_views.player_detail, name='player_detail'),
    
    # Teams
    path('teams/', team_views.team_list, name='team_list'),
    path('teams/<int:pk>/', team_views.team_detail, name='team_detail'),
    
    # Trainings
    path('trainings/', training_views.training_list, name='training_list'),
    path('trainings/<int:pk>/', training_views.training_detail, name='training_detail'),
    
    # Tournaments
    path('tournaments/', tournament_views.tournament_list, name='tournament_list'),
    path('tournaments/<int:pk>/', tournament_views.tournament_detail, name='tournament_detail'),
]