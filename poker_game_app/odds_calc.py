import itertools
import time
from .evaluate_hands import *

deck = ['AH', 'AD', 'AC', 'AS', 'KH', 'KD', 'KC', 'KS', 'QH', 'QD', 'QC', 'QS', 'JH', 'JD', 
            'JC', 'JS', 'TH', 'TD', 'TC', 'TS', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', 
            '7H', '7D', '7C', '7S', '6H', '6D', '6C', '6S', '5H', '5D', '5C', '5S', '4H', '4D', 
            '4C', '4S', '3H', '3D', '3C', '3S', '2H', '2D', '2C', '2S']
num_players = 1

#turn_cards remaining can be 0(here odds are either 0% or 100%), 1 or 2
#hand represents the hand(on ranking from 1 to 10) that player has ex.[5, 10, hand] means straight with 10 high
def get_odds(known_cards, turn_cards_rem, hand): 
    start_time = time.time()
    for card in known_cards:
        deck.remove(card)
    opponent_cards = list(itertools.combinations(deck, 2*num_players))
    win = 0
    loss = 0
    for h in opponent_cards:
        temp_deck = deck
        temp_deck.remove(h[0])
        temp_deck.remove(h[0])
        turn_cards = list(itertools.combinations(temp_deck, turn_cards_rem))
        for t in turn_cards:
            new_hand = [t[0], t[1], h[0], h[1]]
            evaluated_hand = evaluate(h)
            #have to take into account tied hand as well
            if compare_hand(hand, evaluated_hand) == hand:
                win+=1
            else:
                loss+=1
    odds = win/(win + loss)
    print("--- %s seconds ---" % (time.time() - start_time))
    return odds
    



