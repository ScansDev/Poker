import itertools
import random
from typing import List, Tuple, Dict

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def get_numeric_value(self):
        if isinstance(self.value, int):
            return self.value
        value_map = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
        return value_map[self.value]

class Hand:
    HAND_RANKINGS = {
        'Royal Flush': 10,
        'Straight Flush': 9,
        'Four of a Kind': 8,
        'Full House': 7,
        'Flush': 6,
        'Straight': 5,
        'Three of a Kind': 4,
        'Two Pair': 3,
        'One Pair': 2,
        'High Card': 1
    }

    def __init__(self, hole_cards: List[Card], community_cards: List[Card]):
        self.hole_cards = hole_cards
        self.community_cards = community_cards
        self.all_cards = hole_cards + community_cards
        self.hand_name = None
        self.hand_value = None
        self.kickers = []

    def evaluate(self):
        """Evaluate the best 5-card hand possible."""
        all_possible_hands = list(itertools.combinations(self.all_cards, 5))
        best_hand = None
        best_hand_value = -1
        
        for hand in all_possible_hands:
            hand_value, hand_name, kickers = self._evaluate_five_cards(list(hand))
            if hand_value > best_hand_value:
                best_hand = hand
                best_hand_value = hand_value
                self.hand_name = hand_name
                self.hand_value = hand_value
                self.kickers = kickers
        
        return self.hand_value, self.hand_name, self.kickers

    def _evaluate_five_cards(self, cards: List[Card]) -> Tuple[int, str, List[int]]:
        """Evaluate a specific 5-card hand."""
        values = sorted([card.get_numeric_value() for card in cards], reverse=True)
        suits = [card.suit for card in cards]
        
        # Check for flush
        is_flush = len(set(suits)) == 1
        
        # Check for straight
        is_straight = (max(values) - min(values) == 4 and len(set(values)) == 5) or \
                     (values == [14, 5, 4, 3, 2])  # Ace-low straight
        
        # Handle special case of Ace-low straight
        if values == [14, 5, 4, 3, 2]:
            values = [5, 4, 3, 2, 1]

        # Count frequencies of values
        value_counts = {}
        for value in values:
            value_counts[value] = value_counts.get(value, 0) + 1
        
        # Determine hand type and return appropriate value
        if is_flush and is_straight and values[0] == 14:
            return 10, 'Royal Flush', values
        elif is_flush and is_straight:
            return 9, 'Straight Flush', values
        elif 4 in value_counts.values():
            quads = max([v for v, c in value_counts.items() if c == 4])
            kicker = max([v for v, c in value_counts.items() if c == 1])
            return 8, 'Four of a Kind', [quads, kicker]
        elif set(value_counts.values()) == {2, 3}:
            trips = max([v for v, c in value_counts.items() if c == 3])
            pair = max([v for v, c in value_counts.items() if c == 2])
            return 7, 'Full House', [trips, pair]
        elif is_flush:
            return 6, 'Flush', values
        elif is_straight:
            return 5, 'Straight', values
        elif 3 in value_counts.values():
            trips = max([v for v, c in value_counts.items() if c == 3])
            kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
            return 4, 'Three of a Kind', [trips] + kickers
        elif list(value_counts.values()).count(2) == 2:
            pairs = sorted([v for v, c in value_counts.items() if c == 2], reverse=True)
            kicker = max([v for v, c in value_counts.items() if c == 1])
            return 3, 'Two Pair', pairs + [kicker]
        elif 2 in value_counts.values():
            pair = max([v for v, c in value_counts.items() if c == 2])
            kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
            return 2, 'One Pair', [pair] + kickers
        else:
            return 1, 'High Card', values

class Player:
    def __init__(self, name, hand=None, playerStack=0, bet=0, position=None):
        self.name = name
        self.playerStack = playerStack
        self.bet = bet
        self.hand = hand if hand else []
        self.position = position
        self.hand_evaluation = None
        self.folded = False
    
    def get_name(self):
        return self.name
    
    def get_playerStack(self):
        return self.playerStack
    
    def get_hand(self):
        return self.hand
    
    def get_bet(self):
        return self.bet
    
    def get_position(self):
        return self.position
    
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
    
    def evaluate_hand(self, community_cards):
        if not self.hand or not community_cards or self.folded:
            return None
        hand = Hand(self.hand, community_cards)
        self.hand_evaluation = hand.evaluate()
        return self.hand_evaluation

class PokerGame:
    def __init__(self):
        self.players = []
        self.deck = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.small_blind = 0
        self.big_blind = 0
        self.button_pos = 0

    def create_deck(self):
        """Create and shuffle a new deck of cards."""
        values = list(range(2, 11)) + ['Jack', 'Queen', 'King', 'Ace']
        suits = ['Spade', 'Heart', 'Diamond', 'Club']
        self.deck = [Card(value, suit) for value in values for suit in suits]
        random.shuffle(self.deck)

    def deal_cards(self):
        """Deal two cards to each player."""
        for _ in range(2):
            for player in self.players:
                if not player.folded:
                    card = self.deck.pop()
                    player.hand.append(card)

    def deal_community_cards(self, number):
        """Deal specified number of community cards."""
        for _ in range(number):
            self.community_cards.append(self.deck.pop())

    def place_blind_bets(self):
        """Place small and big blind bets."""
        # Small blind
        sb_pos = (self.button_pos + 1) % len(self.players)
        sb_player = self.players[sb_pos]
        sb_amount = min(self.small_blind, sb_player.playerStack)
        sb_player.set_bet(sb_amount)
        sb_player.set_playerStack(sb_player.playerStack - sb_amount)
        
        # Big blind
        bb_pos = (self.button_pos + 2) % len(self.players)
        bb_player = self.players[bb_pos]
        bb_amount = min(self.big_blind, bb_player.playerStack)
        bb_player.set_bet(bb_amount)
        bb_player.set_playerStack(bb_player.playerStack - bb_amount)
        
        self.current_bet = self.big_blind
        self.pot = sb_amount + bb_amount

    def betting_round(self, starting_pos):
        """Execute a betting round."""
        num_active_players = sum(1 for p in self.players if not p.folded)
        if num_active_players < 2:
            return False

        current_pos = starting_pos
        round_complete = False
        players_acted = 0
        
        while not round_complete:
            current_player = self.players[current_pos]
            
            if not current_player.folded:
                print(f"\n{current_player.name}'s turn")
                print(f"Hand: {current_player.hand}")
                print(f"Stack: {current_player.playerStack}")
                print(f"Current bet: {self.current_bet}")
                print(f"Your current bet: {current_player.bet}")
                
                if self.current_bet > current_player.bet:
                    options = ["fold", "call"]
                    if current_player.playerStack > self.current_bet - current_player.bet:
                        options.append("raise")
                else:
                    options = ["check"]
                    if current_player.playerStack > 0:
                        options.append("raise")

                print(f"Options: {', '.join(options)}")
                action = input("Your action: ").lower()

                while action not in options:
                    print(f"Invalid action. Options are: {', '.join(options)}")
                    action = input("Your action: ").lower()

                if action == "fold":
                    current_player.folded = True
                    num_active_players -= 1
                    if num_active_players < 2:
                        return False
                
                elif action == "call":
                    call_amount = min(self.current_bet - current_player.bet, current_player.playerStack)
                    current_player.set_bet(call_amount)
                    current_player.set_playerStack(current_player.playerStack - call_amount)
                    self.pot += call_amount
                
                elif action == "raise":
                    min_raise = self.current_bet * 2
                    max_raise = current_player.playerStack + current_player.bet
                    print(f"Min raise: {min_raise}, Max raise: {max_raise}")
                    raise_to = int(input("Raise to: "))
                    
                    while raise_to < min_raise or raise_to > max_raise:
                        print(f"Invalid raise amount. Must be between {min_raise} and {max_raise}")
                        raise_to = int(input("Raise to: "))
                    
                    raise_amount = raise_to - current_player.bet
                    current_player.set_bet(raise_amount)
                    current_player.set_playerStack(current_player.playerStack - raise_amount)
                    self.current_bet = raise_to
                    self.pot += raise_amount
                    players_acted = 0  # Reset because of raise
                
                elif action == "check":
                    pass
                
                players_acted += 1

            current_pos = (current_pos + 1) % len(self.players)
            
            # Check if round is complete
            if players_acted >= num_active_players:
                all_players_matched = True
                for player in self.players:
                    if not player.folded and player.bet != self.current_bet:
                        all_players_matched = False
                        break
                if all_players_matched:
                    round_complete = True

        return True

    def determine_winners(self) -> List[Tuple[Player, float]]:
        """Determine winners and their share of the pot."""
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) == 1:
            return [(active_players[0], self.pot)]

        # Evaluate all hands
        for player in active_players:
            player.evaluate_hand(self.community_cards)
        
        # Group players by hand value
        players_by_hand = {}
        for player in active_players:
            hand_value = player.hand_evaluation[0]
            if hand_value not in players_by_hand:
                players_by_hand[hand_value] = []
            players_by_hand[hand_value].append(player)
        
        # Find winners
        max_hand_value = max(players_by_hand.keys())
        potential_winners = players_by_hand[max_hand_value]
        
        winners = []
        best_kickers = None
        for player in potential_winners:
            kickers = player.hand_evaluation[2]
            if best_kickers is None or kickers > best_kickers:
                winners = [player]
                best_kickers = kickers
            elif kickers == best_kickers:
                winners.append(player)
        
        # Split pot equally among winners
        share = self.pot / len(winners)
        return [(winner, share) for winner in winners]

    def play_round(self):
        """Play a complete round of poker."""
        # Reset round state
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []
        for player in self.players:
            player.hand = []
            player.bet = 0
            player.folded = False
            player.hand_evaluation = None

        # Create and shuffle deck
        self.create_deck()

        # Place blind bets
        self.place_blind_bets()

        # Deal hole cards
        self.deal_cards()

        # Pre-flop betting round
        if not self.betting_round((self.button_pos + 3) % len(self.players)):
            return self.determine_winners()

        # Flop
        self.deal_community_cards(3)
        print("\nFlop:", self.community_cards)
        if not self.betting_round((self.button_pos + 1) % len(self.players)):
            return self.determine_winners()

        # Turn
        self.deal_community_cards(1)
        print("\nTurn:", self.community_cards)
        if not self.betting_round((self.button_pos + 1) % len(self.players)):
            return self.determine_winners()

        # River
        self.deal_community_cards(1)
        print("\nRiver:", self.community_cards)
        if not self.betting_round((self.button_pos + 1) % len(self.players)):
            return self.determine_winners()

        return self.determine_winners()

    def play_game(self):
            """Start and manage the poker game."""
            print("Welcome to Texas Hold'em Poker!")
            
            # Get number of players
            while True:
                try:
                    num_players = int(input("Enter number of players (2-9): "))
                    if 2 <= num_players <= 9:
                        break
                    print("Please enter a number between 2 and 9.")
                except ValueError:
                    print("Please enter a valid number.")

            # Get player names and buy-in amount
            while True:
                try:
                    buy_in = int(input("Enter buy-in amount: "))
                    if buy_in > 0:
                        break
                    print("Buy-in must be greater than 0.")
                except ValueError:
                    print("Please enter a valid number.")

            # Get blind amounts
            while True:
                try:
                    self.small_blind = int(input("Enter small blind amount: "))
                    self.big_blind = int(input("Enter big blind amount: "))
                    if 0 < self.small_blind < self.big_blind:
                        break
                    print("Small blind must be less than big blind and both must be greater than 0.")
                except ValueError:
                    print("Please enter valid numbers.")

            # Create players
            for i in range(num_players):
                while True:
                    name = input(f"Enter name for Player {i+1}: ").strip()
                    if name and not any(p.name == name for p in self.players):
                        break
                    print("Please enter a unique, non-empty name.")
                
                player = Player(name, playerStack=buy_in)
                self.players.append(player)

            # Main game loop
            round_number = 1
            while len([p for p in self.players if p.playerStack > 0]) > 1:
                print(f"\n{'='*50}")
                print(f"Round {round_number}")
                print(f"{'='*50}")
                
                # Show player stacks
                print("\nPlayer Stacks:")
                for player in self.players:
                    print(f"{player.name}: {player.playerStack}")
                
                # Move button
                self.button_pos = (self.button_pos + 1) % len(self.players)
                print(f"\nDealer button: {self.players[self.button_pos].name}")
                
                # Play round
                winners = self.play_round()
                
                # Display results
                print("\nRound Results:")
                for winner, amount in winners:
                    winner.set_playerStack(winner.playerStack + amount)
                    hand_name = winner.hand_evaluation[1] if winner.hand_evaluation else "by default"
                    print(f"{winner.name} wins {amount:.2f} with {hand_name}")
                
                # Remove players with no chips
                self.players = [p for p in self.players if p.playerStack > 0]
                
                # Ask to continue
                if len(self.players) > 1:
                    choice = input("\nContinue to next round? (y/n): ").lower()
                    if choice != 'y':
                        break
                
                round_number += 1

            # Game over
            print("\nGame Over!")
            print("\nFinal Standings:")
            for player in sorted(self.players, key=lambda p: p.playerStack, reverse=True):
                print(f"{player.name}: {player.playerStack}")

def main():
    """Main function to start the game."""
    while True:
        game = PokerGame()
        game.play_game()
        
        play_again = input("\nWould you like to start a new game? (y/n): ").lower()
        if play_again != 'y':
            break
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
