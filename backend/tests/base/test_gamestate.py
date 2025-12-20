import unittest
from src.game.gamestate import GameState
from src.core.hand import Hand
from src.game.player_range import PlayerRange
from treys import Card

class TestGameState(unittest.TestCase):

    def test_gamestate(self):
        hand = Hand([Card.new('As'), Card.new('Kd')])

        opp_range = PlayerRange('OOP')
        opp_range.add_suited_cards('Q', 'J')


        gs = GameState('IP', hand, opp_range)

        gs.add_community_card(Card.new('2h'))
        gs.add_community_card(Card.new('7h'))
        gs.add_community_card(Card.new('Th'))
        gs.add_community_card(Card.new('3c'))
        gs.add_community_card(Card.new('9d'))

        results = gs.evaluate()
        self.assertEqual(results['wins'], 3) # player should win three times
        self.assertEqual(results['total'], 4) # total of four hands in opponent range

if __name__ == "__main__":
    unittest.main()
        


