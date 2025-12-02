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

        ranges = {'OOP': oop_range, 'IP': ip_range}
        stacks = {'OOP': 1000, 'IP': 1000}
        contributions = {'OOP': 50, 'IP': 50}
        pot = 100

        tree_builder = TreeBuilder(ranges, stacks, contributions, pot)
    
        root_node = tree_builder.create_root_node()
        
        self.assertIsNotNone(root_node)
        self.assertEqual(len(root_node.states), 10)  # 6 (AA) + 4 (KQs) = 10 unique hands
        self.assertEqual(root_node.turn, 'OOP')
        self.assertEqual(root_node.street, 'flop')
        self.assertEqual(root_node.stacks, stacks)
        self.assertEqual(root_node.contributions, contributions)
        self.assertEqual(root_node.pot, pot)

    def test_children_generation(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ranges = {'OOP': oop_range, 'IP': ip_range}
        stacks = {'OOP': 1000, 'IP': 1000}
        contributions = {'OOP': 50, 'IP': 50}
        pot = 100

        tree_builder = TreeBuilder(ranges, stacks, contributions, pot)
    
        root_node = tree_builder.create_root_node()

        tree_builder.create_children(root_node)

        self.assertEqual(len(root_node.children), 3)  # fold, call/check, raise
        self.assertEqual(root_node.children[0].state, 'terminal')  # fold child should be terminal

        # call/check child tests
        self.assertEqual(root_node.children[1].turn, 'IP')    # call/check child should be action
        self.assertEqual(root_node.children[1].pot, pot)
        self.assertEqual(root_node.children[1].stacks, {'OOP': 1000, 'IP': 1000})  # IP called 50

        # raise child tests
        self.assertEqual(root_node.children[2].turn, 'IP')    # raise child should be action
        self.assertEqual(root_node.children[2].pot, 150)
        self.assertEqual(root_node.children[2].stacks, {'OOP': 950, 'IP': 1000})  # OOP raised 50
        self.assertEqual(root_node.children[2].contributions, {'OOP': 100, 'IP': 50})  # OOP contributed 100
        self.assertEqual(root_node.children[2].raise_count, 1)  # raise count should be incremented