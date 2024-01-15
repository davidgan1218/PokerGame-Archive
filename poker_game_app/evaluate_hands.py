from collections import Counter

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0]


#gets card value from  a hand. converts A to 14,  is_seq function will convert the 14 to a 1 when necessary to evaluate A 2 3 4 5 straights
def convert_to_nums(hand):
    nums = {'T':10, 'J':11, 'Q':12, 'K':13, "A": 14}
    for x in range(len(hand)):
        if (hand[x][0]) in nums.keys():
            hand[x] = str(nums[hand[x][0]]) + hand[x][1]

    return hand

# is royal flush
# if a hand is a straight and a flush and the lowest value is a 10 then it is a royal flush
def is_royal_flush(hand):
    new_hand = convert_to_nums(hand)
    if is_seq(hand):
        if is_flush(hand):
            nn = [int(x[:-1]) for x in new_hand]
            if min(nn) == 10:
                return True
    else:
        return False
   
# converts hand to number values and then evaluates if they are sequential  
def is_seq(h):
    ace = False
    r = h[:]

    h = [x[:-1] for x in convert_to_nums(h)]


    h = [int(x) for x in h]
    h = list(sorted(h))
    ref = True
    for x in range(0,len(h)-1):
        if not h[x]+1 == h[x+1]:
            ref =  False
            break

    if ref:
        return True, h[4]

    aces = [i for i in h if str(i) == "14"]
    if len(aces) == 1:
        for x in range(len(h)):
            if str(h[x]) == "14":
                h[x] = 1

    h = list(sorted(h))
    for x in range(0,len(h)-1):
        if not h[x]+1 == h[x+1]:
            return False
    return True, h[4]

# call set() on the suit values of the hand and if it is 1 then they are all the same suit
def is_flush(h):
 suits = [x[-1] for x in h]
 if len(set(suits)) == 1:
  hand = convert_to_nums(h)
  nn = [int(x[:-1]) for x in hand]
  max_num = max(nn)
  return True, max_num
 else:
  return False


# if the most common element occurs 4 times then it is a four of a kind
def is_fourofakind(h):
 h = [a[:-1] for a in h]
 i = Most_Common(h)
 if i[1] == 4:
  return True, int(i[0])
 else:
  return False


# if the most common element occurs 3 times then it is a three of a kind
def is_threeofakind(h):
 h = [a[:-1] for a in h]
 i = Most_Common(h)
 if i[1] == 3:
  return True, int(i[0])
 else:
  return False


# if the first 2 most common elements have counts of 3 and 2, then it is a full house
def is_fullhouse(h):
 h = [a[:-1] for a in h]
 data = Counter(h)
 a, b = data.most_common(1)[0], data.most_common(2)[-1]
 if str(a[1]) == '3' and str(b[1]) == '2':
  return True, int(a[0])
 return False

# if the first 2 most common elements have counts of 2 and 2 then it is a two pair
def is_twopair(h):
 h = [a[:-1] for a in h]
 data = Counter(h)
 a, b = data.most_common(1)[0], data.most_common(2)[-1]
 if str(a[1]) == '2' and str(b[1]) == '2':
  print (a[0], b[0])
  return True, max(int(a[0]), int(b[0]))
 return False


#if the first most common element is 2 then it is a pair
def is_pair(h):
 h = [a[:-1] for a in h]
 data = Counter(h)
 a = data.most_common(1)[0]

 if str(a[1]) == '2':
  return True, int(a[0]) 
 else:
  return False

#get the high card 
def get_high(h):
 return int(list(sorted([int(x[:-1]) for x in convert_to_nums(h)], reverse =True))[0])

# # FOR HIGH CARD or ties, this function compares two hands by ordering the hands from highest to lowest and comparing each card and returning when one is higher then the other
# def compare(xs, ys):
#   xs, ys = list(sorted(xs, reverse =True)), list(sorted(ys, reverse = True))

#   for i, c in enumerate(xs):
#    if ys[i] > c:
#     return 'RIGHT'
#    elif ys[i] < c:
#     return 'LEFT'

#   return "TIE"