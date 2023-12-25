from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    """The structure of the poker game"""

    status = models.IntegerField(default=4) #current status of game
    river_card1 = models.CharField(null = True, max_length=100) 
    river_card2 = models.CharField(null = True, max_length=100) 
    river_card3 = models.CharField(null = True, max_length=100) 
    river_card4 = models.CharField(null = True, max_length=100) 
    river_card5 = models.CharField(null = True, max_length=100) 

    deck = models.CharField(null = True, max_length=512)
    #deck = ['AH', 'AD', 'AC', 'AS', 'KH', 'KD', 'KC', 'KS', 'QH', 'QD', 'QC', 'QS', 'JH', 'JD', 'JC', 'JS', 'TH', 'TD', 'TC', 'TS', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', '7H', '7D', '7C', '7S', '6H', '6D', '6C', '6S', '5H', '5D', '5C', '5S', '4H', '4D', '4C', '4S', '3H', '3D', '3C', '3S', '2H', '2D', '2C', '2S'] 
    min_bet = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    num_players = models.IntegerField(default=0)
    #list_players  = #list of players in the game

class Player(models.Model):
    """Individual player in game, associated with registered user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    chips = models.IntegerField(default=5000)
    point = models.IntegerField(default=0)
    card1 = models.CharField(max_length=10, null = True)
    card2 = models.CharField(max_length=10, null=True)
    status = models.IntegerField(default=0)
    bet = models.IntegerField(default=0)

