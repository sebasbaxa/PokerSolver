from treys import Card
from src.core.hand import Hand

class Range:
    # Represents a range of poker hands.
    # Each hand in the range must contain exactly two unique cards.

    def __init__(self):
        self.hands = []

    def add_hand(self, hand):
        if not isinstance(hand, Hand):
            raise ValueError("Only Hand instances can be added to the range.")
        if hand in self.hands:
            raise ValueError("This hand is already in the range.")

        self.hands.append(hand)
    
    def get_hands(self):
        return self.hands
    
    def __repr__(self):
        return "Range({})".format([str(hand) for hand in self.hands])