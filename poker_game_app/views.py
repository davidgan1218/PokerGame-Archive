from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Player, Game
from .forms import BetForm
from django.http import HttpResponseServerError
from .evaluate_hands import *
import random, json



@api_view(['GET'])
def index(request):
    """The home page for poker_game_app"""
    #return Response({"test": "test"})
    return render(request, 'poker_game_app/index.html')

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
    user = request.user
    
    player_exists = Player.objects.filter(user=user).exists()
    player = None  # Define player outside the if block
    game = None

    try:
        if not player_exists:
            player = Player.objects.create(user=user)
            
            game = Game.objects.create(deck=get_deck())
            player.game = game
            player.save()
        else:
            player = Player.objects.get(user=user)
            game = player.game
            game.deck=get_deck()
            game.save()
            player.game = game
            player.save()

        context = {'player': player}
        return render(request, 'poker_game_app/lobby.html', context)
        #return Response({'player': "HI"})
    except Exception as e: 
        return HttpResponseServerError(f"An error occurred: {e}")

@login_required
def in_game(request, player_id):
    
    player = Player.objects.get(id=player_id)
    game = player.game
    #Initialization of variables
    game.status = 0
    game.deck = get_deck()
    player.card1 = None
    player.card2 = None
    game.pot = 0
    game.river_card1 = None
    game.river_card2 = None
    game.river_card3 = None
    game.river_card4 = None
    game.river_card5 = None

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
    game.status += 1
    game.save()
    player.save()

    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/check.html', context)

@login_required
def bet(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = form.cleaned_data['bet']
            game.pot += bet
            player.chips -= bet
            #game.status += 1
            game.save()
            player.save()
            print("HIHIHIHIH")
            print(game.status)
            return redirect('poker_game_app:check', player_id=player.id)
    else:
        form = BetForm()

    context = {'player': player, 'game': game, 'form': form}
    return render(request, 'poker_game_app/bet.html', context)

@login_required
def fold(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game
    game.status = 0
    game.save()
    player.save()

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

@login_required
def turn_card1(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game

    deck = json.loads(game.deck)

    card = deck[0]
    del deck[0]
    game.river_card4 = card
    game.deck = json.dumps(deck)
    game.save()

    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/turn_card1.html', context)

@login_required
def turn_card2(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game

    deck = json.loads(game.deck)

    card = deck[0]
    del deck[0]
    game.river_card5 = card
    game.deck = json.dumps(deck)
    game.save()

    context = {'player': player, 'game': game}

    return render(request, 'poker_game_app/turn_card2.html', context)


@login_required
def reveal_hand(request, player_id):
    player = Player.objects.get(id=player_id)
    game = player.game
   
    cards = [player.card1, player.card2, game.river_card1, game.river_card2, game.river_card3, game.river_card4, game.river_card5]
    # print(cards)
    all_hands = get_hands(cards) #this will store all the 21 possible hands you can make with 2 hand cards + 5 river cards
    # print(all_hands)
    best_hand = [0, 0, []]

    for hand in all_hands:

        cur_hand = evaluate(hand) #returns what the hand is, including hand type(integer from 1-10) and identifier(2 - A)
        # print("Cur_hand: ", cur_hand)
        # print("Best_hand_before: ", best_hand)
        best_hand = compare_hand(best_hand, cur_hand) # compare with current best hand
        #print("Best_hand_after: ", best_hand)
    
    player.hand_text = translate(best_hand[0])
    player.hand_num = best_hand[1]
    player.save()

    context = {'player' : player}

    return render(request, 'poker_game_app/reveal_hand.html', context)

