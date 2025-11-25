import unittest
from src.tree.id import create_ids, get_hand_from_id
from src.game.player_range import PlayerRange

class TestCreateIds(unittest.TestCase):

    def test_create_ids(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ids = create_ids(oop_range, ip_range)
        self.assertEqual(len(ids), 10) # there should be 6 (AA) + 4 (KQs) = 10 unique IDs

        duplicate_check = set(ids)
        self.assertEqual(len(duplicate_check), len(ids))  # Ensure all IDs are unique

    def test_get_hand_from_id(self):
        hand_id = "OOPAsKd"
        hand = get_hand_from_id(hand_id) 
        self.assertEqual(str(hand), "AsKd")  # Check if the reconstructed hand matches the original
        



if __name__ == "__main__":
    unittest.main()