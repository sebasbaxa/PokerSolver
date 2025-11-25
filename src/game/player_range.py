from treys import Card
from src.core.range import Range
from src.core.hand import Hand


class PlayerRange:
    # Represents the range of hand for a specific id

    def __init__(self, id):
        self.id = id  # 'OOP' or 'IP'
        self.range = Range()
    
    def add_hand(self, hand):
        if not isinstance(hand, Hand):
            raise ValueError("Only Hand instances can be added to the player range.")
        if hand in self.range.get_hands():
            raise ValueError("This hand is already in the player range.")

        self.range.add_hand(hand)
    
    def get_hands(self):
        return self.range.get_hands()

    def add_pocket_pair(self, rank):
        # Adds all combinations of pocket pairs for the given rank to the range
        suits = ['h', 'd', 'c', 's']
        for i in range(len(suits)):
            for j in range(i + 1, len(suits)):
                hand = Hand()
                hand.add_card(Card.new(rank + suits[i]))
                hand.add_card(Card.new(rank + suits[j]))
                self.add_hand(hand)
    
    def add_suited_cards(self, rank1, rank2):
        # Adds all combinations of suited cards for the given ranks to the range
        suits = ['h', 'd', 'c', 's']
        for suit in suits:
            hand = Hand()
            hand.add_card(Card.new(rank1 + suit))
            hand.add_card(Card.new(rank2 + suit))
            self.add_hand(hand)
    
    def add_offsuit_cards(self, rank1, rank2):
        # Adds all combinations of offsuit cards for the given ranks to the range
        suits = ['h', 'd', 'c', 's']
        for i in range(len(suits)):
            for j in range(len(suits)):
                if i != j:
                    hand = Hand()
                    hand.add_card(Card.new(rank1 + suits[i]))
                    hand.add_card(Card.new(rank2 + suits[j]))
                    self.add_hand(hand)

    def __repr__(self):
        return "PlayerRange(id={}, range={})".format(self.id, str(self.range))
    
