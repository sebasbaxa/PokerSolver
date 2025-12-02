from treys import Evaluator, Card
from src.core.deck import Deck
from src.core.hand import Hand
from src.core.range import Range
from src.game.player_range import PlayerRange


class GameState:
    # Represents the current state of a poker game for one position
    # The current palyer knows their hand and the community cards, but are modeled against an opponent range

    def __init__(self, player, player_hand, opponent_range):
        # initialize the deck and empty community cards and player hands
        self.deck = Deck()
        self.community_cards = []

        self.player = player # 'OOP' or 'IP'
        self.player_hand = player_hand

        self.opponent_range = opponent_range

        # starting values
        self.regret = {"call":0.33, "raise":0.33, "fold":0.33}
        self.strategy = {"call":0.33, "raise":0.33, "fold":0.33}
        self.ev = {"call":0.33, "raise":0.33, "fold":0.33}

        self.pot = 0

    def set_opponent_range(self, opponent_range) -> None:
        if not isinstance(opponent_range, PlayerRange):
            raise ValueError("Opponent range must be a PlayerRange instance.")
        if opponent_range.id == self.player:
            raise ValueError("Opponent range ID must be different from the player's ID.")

        self.opponent_range = opponent_range

    def add_player_hand(self, hand) -> None:
        if not isinstance(hand, Hand):
            raise ValueError("Only Hand instances can be added as player hand.")
        
        self.player_hand = hand
        # remove the player's cards from the deck
        for card in hand.cards:
            self.deck.remove_card(card)

    def add_community_card(self, card) -> None:
        self.community_cards.append(card)
        self.deck.remove_card(card)
    
    def evaluate(self) -> dict:
        evaluator = Evaluator()
        player_score = evaluator.evaluate(self.player_hand.cards, self.community_cards)

        player_wins = 0
        ties = 0
        total = 0

        for opponent_hand in self.opponent_range.get_hands():
            opponent_score = evaluator.evaluate(opponent_hand.cards, self.community_cards)
            total += 1
            if player_score < opponent_score:
                player_wins += 1
            elif player_score == opponent_score:
                ties += 1

        # return the results of the players hand against the opponent range
        return {
                'wins': player_wins,
                'ties': ties,
                'total': total,
                }

    

        

        

    
    
