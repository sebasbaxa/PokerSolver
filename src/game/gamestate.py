from treys import Evaluator, Card
from src.core.deck import Deck
from src.core.hand import Hand


class GameState:
    # Represents the current state of a poker game.
    # This includes the deck, community cards, and two players hands.

    def __init__(self):
        # initialize the deck and empty community cards and player hands
        self.deck = Deck()
        self.community_cards = []

        self.OOP_hand = Hand()
        self.OOP_stack = 0
        self.OOP_contribution = 0

        self.IP_hand = Hand()
        self.IP_stack = 0
        self.IP_contribution = 0

        self.pot = 0


    def add_hand(self, hand, id):
        # add a hand for the specified player and remove the cards from the deck
        if not isinstance(hand, Hand):
            raise ValueError("Only Hand instances can be added as player hands.")

        self.deck.remove_hand(hand)

        if id == 'OOP':
            self.OOP_hand = hand
        elif id == 'IP':
            self.IP_hand = hand
        else:
            raise ValueError("Invalid player ID. Use 'OOP' or 'IP'.")
    

    def add_bet(self, amount, id):
        # add a bet for the specified player and update their stack and contribution
        if id == 'OOP':
            if amount > self.OOP_stack:
                raise ValueError("OOP does not have enough stack to bet this amount.")
            self.OOP_stack -= amount
            self.OOP_contribution += amount
        elif id == 'IP':
            if amount > self.IP_stack:
                raise ValueError("IP does not have enough stack to bet this amount.")
            self.IP_stack -= amount
            self.IP_contribution += amount
        else:
            raise ValueError("Invalid player ID. Use 'OOP' or 'IP'.")

        self.pot += amount


    def add_community_card(self, card):
        # add a card to the community cards and remove it from the deck
        if not card in self.deck.cards:
            raise ValueError("This card is not available in the deck.")
        
        self.deck.remove_card(card)
        
        self.community_cards.append(card)


    def evaluate(self):
        # if there are not enough community cards, return None
        if len(self.community_cards) < 5:
            return None
        
        evaluator = Evaluator()
        OOP_score = evaluator.evaluate(self.community_cards, self.OOP_hand.cards)
        IP_score = evaluator.evaluate(self.community_cards, self.IP_hand.cards)

        # return the ID if the player with the better hand, else return 'TIE'
        if OOP_score < IP_score:
            return 'OOP'
        elif IP_score < OOP_score:
            return 'IP'
        else:
            return 'TIE'

    
    
