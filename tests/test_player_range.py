import unittest
from src.game.player_range import PlayerRange
from treys import Card

class TestPlayerRange(unittest.TestCase):

    def test_pocket_pair(self):
        player_range = PlayerRange('OOP')
        player_range.add_pocket_pair('A')

        self.assertEqual(len(player_range.range.get_hands()), 6)  # 6 combinations of pocket Aces

    def test_suited_cards(self):
        player_range = PlayerRange('IP')
        player_range.add_suited_cards('K', 'Q')

        self.assertEqual(len(player_range.range.get_hands()), 4)  # 4 combinations of suited KQs
    
    def test_offsuit_cards(self):
        player_range = PlayerRange('OOP')
        player_range.add_offsuit_cards('J', 'T')

        self.assertEqual(len(player_range.range.get_hands()), 12)  # 12 combinations of offsuit JTs

if __name__ == "__main__":
    unittest.main()