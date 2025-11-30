import unittest
from src.tree.tree_builder import TreeBuilder
from src.game.player_range import PlayerRange


class TestCreateRootNode(unittest.TestCase):

    # Test that the root node is being created correctly with the correct number of gamestates
    def test_create_root_node(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        tree_builder = TreeBuilder(oop_range, ip_range)
        root_node = tree_builder.create_root_node(
            OOP_stack=1000,
            IP_stack=1000,
            OOP_contribution=50,
            IP_contribution=50,
            pot=100
        )
        
        self.assertIsNotNone(root_node)
        self.assertEqual(len(root_node.states), 10)  # 6 (AA) + 4 (KQs) = 10 unique hands

