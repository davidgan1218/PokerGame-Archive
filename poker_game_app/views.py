from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Player, Game
from .forms import BetForm
import random, json



def index(request):
    """The home page for poker_game_app"""
    return render(request, 'poker_game_app/index.html')


# @login_required
# def player_index(request):
#     """The home page for a player once they log in"""

#     # Try to get the Player object for the logged-in user
#     player, created = Player.objects.get_or_create(user=request.user)

#     context = {'player': player}
#     return render(request, 'poker_game_app/player_index.html', context)


def get_deck():
    deck = ['AH', 'AD', 'AC', 'AS', 'KH', 'KD', 'KC', 'KS', 'QH', 'QD', 'QC', 'QS', 'JH', 'JD', 
            'JC', 'JS', 'TH', 'TD', 'TC', 'TS', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', 
            '7H', '7D', '7C', '7S', '6H', '6D', '6C', '6S', '5H', '5D', '5C', '5S', '4H', '4D', 
            '4C', '4S', '3H', '3D', '3C', '3S', '2H', '2D', '2C', '2S']
    random.shuffle(deck)
    return json.dumps(deck)


@login_required
def lobby(request):
    """Lobby Screen"""
    player, created = Player.objects.get_or_create(user=request.user)
    game = ''
    if len(Game.objects.all()) == 0:
        game=Game(deck=get_deck())
        game.save()
    else:
        game = Game.objects.filter(status=4)[0]
    
    #player = Player.objects.get(id=player_id)
    player.game = game
    player.save()

    context = {'game': game, 'player': player}
    return render(request, 'poker_game_app/lobby.html', context)

@login_required
def in_game(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game
    deck = json.loads(game.deck)
    random.shuffle(deck)
    card0 = deck[0]
    card1 = deck[1]
    del deck[0]
    del deck[0]
    player.card1 = card0
    player.card2 = card1
    game.deck = json.dumps(deck)
    player.save()
    game.save()
    
    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/in_game.html', context)

@login_required
def check(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game

    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/check.html', context)

@login_required
def bet(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game
    #form = BetForm()

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = form.cleaned_data['bet']
            game.pot += bet
            player.chips -= bet
            player.save()
            game.save()
            return redirect('poker_game_app:river_cards', player_id=player.id)
    else:
        form = BetForm()

    context = {'player': player, 'game': game, 'form': form}
    return render(request, 'poker_game_app/bet.html', context)

@login_required
def fold(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game

    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/fold.html', context)

@login_required
def river_cards(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game

    deck = json.loads(game.deck)
    
    card0 = deck[0]
    card1 = deck[1]
    card2 = deck[2]
    del deck[0]
    del deck[0]
    del deck[0]
    game.river_card1 = card0
    game.river_card2 = card1
    game.river_card3 = card2

    game.deck = json.dumps(deck)
    game.save()

    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/river_cards.html', context)

    