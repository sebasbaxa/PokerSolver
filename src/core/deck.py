from treys import Card


class Deck:
    # Represents a standard deck of 52 playing cards.
    # Initializes with all cards in the deck.
    # Each card can be removed individually or as part of a hand.
    
    def __init__(self):
        self.cards = []

        suits = ['h', 'd', 'c', 's']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card.new(rank + suit))
    
    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError("This card is not in the deck.")
        
    def remove_hand(self, hand):
        for card in hand.cards:
            self.remove_card(card)
    
    def __repr__(self):
        return "Deck({})".format([Card.int_to_pretty_str(card) for card in self.cards])
