import unittest
from src.tree.create_states import create_ids
from src.game.player_range import PlayerRange

class TestCreateIds(unittest.TestCase):

    def test_create_ids(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ids = create_ids(oop_range, ip_range)
        self.assertEqual(len(ids), 24)  # 6 combinations of AA * 4 combinations of KQs = 24 unique IDs

        duplicate_check = set(ids)
        self.assertEqual(len(duplicate_check), len(ids))  # Ensure all IDs are unique

if __name__ == "__main__":
    unittest.main()