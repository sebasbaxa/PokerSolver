import sys
import unittest
from src.tree.tree_builder import TreeBuilder
from src.game.player_range import PlayerRange
from src.tree.children_gen import create_fold_child, create_call_child, create_raise_child


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
    
    def test_re_raise_nodes(self):
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
        raise1 = create_raise_child(root_node)  # OOP raises
        root_node.children.append(raise1)
        raise2 = create_raise_child(raise1)    # IP re-raises
        raise1.children.append(raise2)
        raise3 = create_raise_child(raise2)    # OOP re-re-raises
        raise2.children.append(raise3) # this child should now be on the next street
        self.assertEqual(raise3.street, 'turn')
        self.assertEqual(raise3.raise_count, 0)  # raise count should reset on new street
        self.assertEqual(raise3.turn, 'OOP')
        self.assertEqual(raise3.contributions['OOP'], raise3.contributions['IP'])  # contributions should be equal after re-re-raise
    
    def test_recursive_tree_generation(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ranges = {'OOP': oop_range, 'IP': ip_range}
        stacks = {'OOP': 500, 'IP': 500}
        contributions = {'OOP': 50, 'IP': 50}
        pot = 100

        tree_builder = TreeBuilder(ranges, stacks, contributions, pot)
    
        tree_builder.generate_tree()

        self.assertIsNotNone(tree_builder.root)

        def dfs_count_children(node):
            if node.state == 'terminal':
                return
            self.assertEqual(len(node.children), 3)  # each non-terminal node should have 3 children
            for child in node.children:
                dfs_count_children(child)

        # check all non-terminal nodes have 3 children
        dfs_count_children(tree_builder.root)
