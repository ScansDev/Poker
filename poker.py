import itertools, random

class Player:
    def __init__(self, name, hand=None, playerStack=0, bet=0, position=None):
        self.name = name
        self.playerStack = playerStack
        self.bet = bet
        if hand is not None:
            self.hand = hand
    def get_name(self):
        return self.name
    def get_playerStack(self):
        return self.playerStack
    def get_hand(self):
        return self.hand
    def get_bet(self):
        return self.bet
    def get_position(self):
        return self.get_position
    def set_name(self, name):
        self.name = name
    def set_playerStack(self, playerStack):
        self.playerStack = playerStack
    def set_hand(self, hand):
        self.hand = hand
    def set_bet(self, bet):
        self.bet += bet
    def set_position(self, position):
        self.position = position


def shuffle_deck(deck):
    random.shuffle(deck)
def create_side_pot(players):
    sidePotPlayers = [players]
    sidePotBet = 0
    return sidePotPlayers, sidePotBet
def play_round(players, smallBlind, bigBlind):
    pot = 0
    folded_players = []
    # Shuffle cards
    my_deck = list(itertools.product(range(2,11),['Spade','Heart','Diamond','Club'])) + list(itertools.product(['Jack', 'Queen', 'King', 'Ace'], ['Spade','Heart','Diamond','Club']))
    print("The cards are being shuffled")
    shuffle_deck(my_deck)
    # Deal Cards
    print("Dealing Cards")
    for j in range(-2,(len(players) - 1) * 2):
        if j < 0:
            players[j].hand = [my_deck[0]]
            my_deck.remove(my_deck[0])
        elif j < len(players) - 2:
            players[j%len(players)].hand = [my_deck[0]]
            my_deck.remove(my_deck[0])
        else:
          players[j%len(players)].hand += [my_deck[0]]
          my_deck.remove(my_deck[0])
    # Designate small and Big Blind
    print("{small_blind} you are small blind and {big_blind} you are big blind".format(small_blind=players[-2].get_name(), big_blind=players[-1].get_name()))

    # Begin pre-flop betting
    players[-2].set_bet(smallBlind)
    players[-2].set_playerStack(players[-2].get_playerStack() - smallBlind)
    players[-1].set_bet(bigBlind)
    players[-1].set_playerStack(players[-1].get_playerStack() - bigBlind)
    highBet = bigBlind
    cardsInPlay = []
    pot = smallBlind + bigBlind
    #player turn function
    def turn(playerTurn, i, highBet, pot):
        if playerChoice == "fold":
            folded_players.append(players.remove(playerTurn))
            if i < 0:
                i += 1
        elif playerChoice == "call":
            if highBet > playerTurn.get_playerStack():
                playerTurn.set_bet(playerTurn.get_playerStack())
                playerTurn.set_playerStack(0)
                pot += playerTurn.get_playerStack()
            else:
                playerTurn.set_bet(highBet)
                playerTurn.set_playerStack(playerTurn.get_playerStack() - highBet)
                pot += highBet
            i += 1
        elif playerChoice == "raise":
            bet = int(input("Enter Raise (Max Raise is {playerStack}): ".format(playerStack=playerTurn.get_playerStack())))
            if bet > playerTurn.get_playerStack():
                playerTurn.set_bet(playerTurn.get_playerStack())
                highBet = playerTurn.get_playerStack()
                pot += playerTurn.get_playerStack()
                playerTurn.set_playerStack(0)
            else:
                playerTurn.set_bet(bet)
                pot += bet
                highBet = bet
                playerTurn.set_playerStack(playerTurn.get_playerStack() - bet)
            i += 1

        elif playerChoice == "check":
            i += 1
        return i, highBet, pot
    i = 0
    while (players[i].get_bet() != highBet or i < len(players)) and len(players) > 1:
        playerTurn = players[i]
        print("{num}'s turn".format(num=playerTurn.get_name()))
        print("{num}'s hand: {playerHand} {num}'s stack: {playerStack}".format(num=playerTurn.get_name(), playerHand=playerTurn.get_hand(), playerStack=playerTurn.get_playerStack()))
        if playerTurn.get_bet() < highBet:
            playerChoice = input("Would you like to fold, call({betSize}) or raise: ".format(betSize=highBet))
        elif playerTurn.get_bet() == highBet:
            playerChoice = input("Would you like to check or raise: ")
        i, highBet, pot = turn(playerTurn, i, highBet, pot)
        if i == len(players):
            break
    #end of pre flop betting
    my_deck.remove(my_deck[0])
    for i in range(3):
        cardsInPlay += [my_deck[0]]
        my_deck.remove(my_deck[0])
    print("\n\n")
    print(cardsInPlay)
    print("\n\n")
    i = -2
    while len(players) > 1 and (players[i].get_bet() != highBet or i < len(players))  :
        playerTurn = players[i]
        highBet = 0
        print("{num}'s turn".format(num=playerTurn.get_name()))
        print("{num}'s hand: {playerHand} {num}'s stack: {playerStack}".format(num=playerTurn.get_name(), playerHand=playerTurn.get_hand(), playerStack=playerTurn.get_playerStack()))
        if playerTurn.get_bet() < highBet:
            playerChoice = input("Would you like to fold, call({betSize}) or raise: ".format(betSize=(highBet-playerTurn.get_bet())))
        elif playerTurn.get_bet() == highBet:
            playerChoice = input("Would you like to check or raise: ")
        i, highBet, pot = turn(playerTurn, i, highBet, pot)
        if i == len(players) - 2:
            break
    # Round Winner
    if len(players) == 1:
        print("{player} won {potSize} chips with a hand of {hand}".format(player=players[0].get_name(), potSize=pot, hand=players[0].get_hand()))
        players[0].set_playerStack(pot)
        pot = 0
    return players
def play_game():
    print("Welcome To Scanlan's Texas Hold'em")
    numPlayers = int(input("Please enter how many players will be at the table (4-9):"))
    while numPlayers < 4 or numPlayers > 9:
        numPlayers = int(input("The number of players you entered is not within the table range, please enter a number between 4-9:"))
    players = []
    for i in range(numPlayers):
        name = str(input("Enter player" + str(i + 1) + " name: "))
        tableName = name 
        print(tableName)
        players.append(Player(tableName))
    tableBuyIn = int(input("What is the buy-in for your table?: "))
    tableStakes = str(input("What are the table stakes (sb/bb): "))
    smallBlind = int(tableStakes.split("/")[0])
    bigBlind = int(tableStakes.split("/")[1])
    for player in players:
        player.set_playerStack(tableBuyIn)
        print(player.get_playerStack())
    play_round(players, smallBlind, bigBlind)

play_game()