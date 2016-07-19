from random import randint

# Complete deck of 52 cards in a list
complete_deck = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A']
# Variable initialization to begin the game
another_round = 'yes'

# Player class
class Player(Plays):
    def __init__(self):
        Plays.__init__(self)
        self.chips = 10
        self.hand = []
# hit function gets a new card, put Aces at the end of the list
    def hit(self, card):
        if card == 'A':
            self.hand.append(card)
        else:
            self.hand.insert(0, card)

# Dealer class
class Dealer(Plays):
    def __init__(self):
        Plays.__init__(self)
        self.hand = []

    def hit(self, card):
        self.hand.append(card)

# Deck class
class Deck(object):
    def __init__(self):
        self.cards = complete_deck.copy()
# reset function is used to refill the deck when is almost empty
    def reset(self):
        self.cards = complete_deck.copy()

player = Player()
dealer = Dealer()
deck = Deck()

# Function to place bet
def place_bet():
    while True:
        try:
            print("\nYou have: %s chips" % player.chips)
            bet = int(input("Place your bet: "))
            if bet < 0 or bet > player.chips:
                continue
        except:
            print("Only numbers")
            continue
        else:
            player.chips -= bet
            print("Total chips: ", player.chips)
            return bet

# Function for draw cards
def draw_card(cards):
    for card in range(cards):
        if(card<2): # Looks for player, is used for the first draw (first 2 cards)
            turn = player
        else: # Looks for dealer
            turn = dealer
        card_index = randint(0, len(deck.cards)-1) # Looks for a random card index in the deck list
        turn.hit(deck.cards[card_index])
        deck.cards.pop(card_index)

# Function that prints the current hand of dealer and player
def print_table(results = False):
    print("\n========================================")
    if results == False: # Doesn't show the dealer's first card
        print("Dealer's hand: [?, %s], " % dealer.hand[1])
    else:
        print("Dealer's hand: ", dealer.hand)
    print("\nPlayer's hand: ", player.hand)
    print("========================================")

# Function that counts the hand
def count(turn):
    point = 0
    for card in turn.hand:
        if card in ['J', 'K', 'Q']:
            point += 10
        elif card == 'A' and point < 11:
            point += 11
        elif card == 'A' and point > 10:
            point += 1
        else:
            point += card
    return point

# Discard hand after every match
def discard():
    player.hand = []
    dealer.hand = []

# Shows the final result
def result(victory, bet):
    if victory == True:
        print("\nYOU WON!")
        print("You won %s chips" % (bet*2))
        player.chips += bet*2
        print("You have %s chips" % player.chips)
    elif victory == False:
        print("\nYOU LOSE!")
        print("You have %s chips" % player.chips)
    else:
        print("\nDRAW!")
        print("You get %s chips" % bet)
        player.chips += bet
        print("You have %s chips" % player.chips)

# This ASCII cards is commented because some IDEs can't print it right
print("Welcome to the Blackjack Game")
# print("┌─────────┐  ┌─────────┐")
# print("│A        │  │K        │")
# print("│         │  │         │")
# print("│    ♠    │  │    ♦    │")
# print("│         │  │         │")
# print("│       A │  │       K │")
# print("└─────────┘  └─────────┘")

# Main code
while another_round == 'yes' and player.chips > 0: # Play until the player is out of chips or when says no
    bet = place_bet() 
    draw_card(4) # Draw 2 cards for each one
    if count(player) == 21: # Check for Blackjack
        print_table(True)
        print("\nBLACKJACK!!!")
        result(True, bet)
    else:
        while True:
            print_table() 
            try:
                option = int(input("\nSelect your move(1 or 2):\n1. Hit\n2. Stand\n> ")) # Select hit or stand
                if option < 1 or option > 2:
                    continue # Loops if choice is not valid
            except:
                print("Select 1 or 2")
                continue
            if option == 2: # Stand option
                break
            elif option == 1: # Hit option
                draw_card(1) 
                if count(player) > 21: # Check if hand is above 21
                    break
        if count(player) > 21 or count(player) < count(dealer): # Check if player loses
            print_table(True)
            result(False, bet)
        elif count(player) == count(dealer): # Check if draw
            result(None, bet)
        else: # Check if player wins
            print_table(True) 
            result(True, bet)
    discard() # Discard hand
    if len(deck.cards) < 6: # Check if deck is almost empty
        deck.reset()
        print("NEW DECK")
    if player.chips > 0: # Ask if wanna continue playing
        another_round = input("\nWanna play another round? (yes or no) ")
print("\nThanks for playing (✿ =‿‿=)")
