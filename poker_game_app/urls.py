"""Defines URL patterns for poker_game_app"""

from django.urls import path
from . import views

app_name = 'poker_game_app'

urlpatterns = [
    #Home Page
    path('', views.index, name='index'),
    path('lobby/', views.lobby, name='lobby'),
    path('in_game/<int:player_id>/', views.in_game, name='in_game'),
    path('check/<int:player_id>/', views.check, name='check'),
    path('bet/<int:player_id>/', views.bet, name='bet'),
    path('fold/<int:player_id>/', views.fold, name='fold'),
    path('river_cards/<int:player_id>', views.river_cards, name="river_cards"),
]
