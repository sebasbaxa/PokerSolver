import unittest
from src.tree.tree_builder import TreeBuilder
from src.game.player_range import PlayerRange
from src.cfr.winrates import calculate_winrates
from src.cfr.cfr import CFRSolver
from treys import Card

class TestCFR(unittest.TestCase):

    def test_calculate_values(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ranges = {'OOP': oop_range, 'IP': ip_range}
        stacks = {'OOP': 1000, 'IP': 1000}
        contributions = {'OOP': 50, 'IP': 50}
        pot = 100

        flop = [Card.new('2h'), Card.new('7h'), Card.new('Th')]

        tree_builder = TreeBuilder(ranges, stacks, contributions, pot, flop)
    
        tree_builder.generate_tree()

        cfr_solver = CFRSolver(tree_builder.root)
        cfr_solver.calc_values(tree_builder.root)

        def dfs(node):
            if node.state == 'showdown' or node.state == 'fold':
                return
            self.assertEqual(len(node.states), 10)  # each node should have 10 gamestates
            self.assertEqual(len(node.children), 3)  # each non-terminal node should have 3 children
            for child in node.children.values():
                dfs(child)

        dfs(tree_builder.root)

    
    def test_calculate_stratagy(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ranges = {'OOP': oop_range, 'IP': ip_range}
        stacks = {'OOP': 1000, 'IP': 1000}
        contributions = {'OOP': 50, 'IP': 50}
        pot = 100

        flop = [Card.new('2h'), Card.new('7h'), Card.new('Th')]

        tree_builder = TreeBuilder(ranges, stacks, contributions, pot, flop)
    
        tree_builder.generate_tree()

        cfr_solver = CFRSolver(tree_builder.root)
        cfr_solver.calc_values(tree_builder.root)
        cfr_solver.recalc_strategies(tree_builder.root)
        
        print(tree_builder.root.states)