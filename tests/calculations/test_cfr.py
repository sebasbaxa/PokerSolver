import unittest
from src.tree.tree_builder import TreeBuilder
from src.game.player_range import PlayerRange
from src.cfr.winrates import create_win_cache
from src.cfr.cfr import CFRSolver
from treys import Card
from cli.traverse_func import traverse_tree

class TestCFR(unittest.TestCase):

    def test_IP_values(self):
        oop_range = PlayerRange('OOP')
        oop_range.add_pocket_pair('A')  # AA

        ip_range = PlayerRange('IP')
        ip_range.add_suited_cards('K', 'Q')  # KQs

        ranges = {'OOP': oop_range, 'IP': ip_range}
        stacks = {'OOP': 1000, 'IP': 1000}
        contributions = {'OOP': 50, 'IP': 50}
        pot = 100

        flop = [Card.new('Th'), Card.new('Jc'), Card.new('8h')]

        tree_builder = TreeBuilder(ranges, stacks, contributions, pot, flop)

        tree_builder.generate_tree()
        root_node = tree_builder.root
        win_cache = create_win_cahce(ip_range, oop_range, root_node)
        cfr_solver = CFRSolver(root_node, win_cache)


        for _ in range(500):
            cfr_solver.calc_stratagy(root_node, 'IP')
            cfr_solver.calc_stratagy(root_node, 'OOP')
            cfr_solver.propagate_reach(root_node)
            cfr_solver.calc_IP_values(root_node)
            cfr_solver.calc_OOP_values(root_node)
        
        traverse_tree(root_node)