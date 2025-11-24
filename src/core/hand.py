from treys import Card

class Hand:
    # Represents a specific hand of two playing cards.
    # Must contain exactly two unique cards.

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        if len(self.cards) >= 2:
            raise ValueError("A hand can only contain two cards.")
        if card in self.cards:
            raise ValueError("This card is already in the hand.")
        
        self.cards.append(card)

    def __repr__(self):
        return "Hand({})".format([Card.int_to_str(card) for card in self.cards])

    


