from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    """The structure of the poker game"""

    status = models.IntegerField(default=0) #current status of game
    river_card1 = models.CharField(null = True, max_length=100) 
    river_card2 = models.CharField(null = True, max_length=100) 
    river_card3 = models.CharField(null = True, max_length=100) 
    river_card4 = models.CharField(null = True, max_length=100) 
    river_card5 = models.CharField(null = True, max_length=100) 

    deck = models.CharField(null = True, max_length=512)
    min_bet = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    num_players = models.IntegerField(default=0)

class Player(models.Model):
    """Individual player in game, associated with registered user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)

    chips = models.IntegerField(default=5000)
    point = models.IntegerField(default=0)
    card1 = models.CharField(max_length=10, null=True)
    card2 = models.CharField(max_length=10, null=True)
    status = models.IntegerField(default=0)
    bet = models.IntegerField(default=0)
    hand_text = models.CharField(max_length = 50, null=True) # textual representation of hand (eg. "full house")
    hand_num = models.IntegerField(null=True) # numerical representation of text

