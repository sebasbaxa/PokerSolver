import unittest
from src.tree.tree_builder import TreeBuilder
from src.game.player_range import PlayerRange
from src.cfr.winrates import create_win_cache
from treys import Card

class TestCalculateWinrates(unittest.TestCase):

    def test_calculate_winrates(self):
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

        root_node = tree_builder.create_root_node()

        winrates = create_win_cache(ip_range, oop_range, root_node)
        print(winrates)


if __name__ == "__main__":
    unittest.main()