import unittest
from src.game.gamestate import GameState
from src.core.hand import Hand
from treys import Card

class TestGameState(unittest.TestCase):

    def test_add_hands(self):
        game = GameState()
        self.assertIsInstance(game.deck, object)
        self.assertEqual(len(game.community_cards), 0)
        self.assertIsInstance(game.OOP_hand, object)
        self.assertIsInstance(game.IP_hand, object)

        hand1 = Hand()
        hand1.add_card(Card.new('As'))
        hand1.add_card(Card.new('Kd'))

        game.add_hand(hand1, 'OOP')
        self.assertEqual(game.OOP_hand, hand1)
        self.assertNotIn(Card.new('As'), game.deck.cards)
        self.assertNotIn(Card.new('Kd'), game.deck.cards)

        hand2 = Hand()
        hand2.add_card(Card.new('Qc'))
        hand2.add_card(Card.new('Jh'))
        game.add_hand(hand2, 'IP')
        self.assertEqual(game.IP_hand, hand2)
        self.assertNotIn(Card.new('Qc'), game.deck.cards)
        self.assertNotIn(Card.new('Jh'), game.deck.cards)
    
    def test_add_community_cards_and_evaluate(self):
        game = GameState()
        self.assertIsInstance(game.deck, object)
        self.assertEqual(len(game.community_cards), 0)
        self.assertIsInstance(game.OOP_hand, object)
        self.assertIsInstance(game.IP_hand, object)

        hand1 = Hand()
        hand1.add_card(Card.new('As'))
        hand1.add_card(Card.new('Kd'))

        game.add_hand(hand1, 'OOP')
        self.assertEqual(game.OOP_hand, hand1)
        self.assertNotIn(Card.new('As'), game.deck.cards)
        self.assertNotIn(Card.new('Kd'), game.deck.cards)

        hand2 = Hand()
        hand2.add_card(Card.new('Qc'))
        hand2.add_card(Card.new('Jh'))
        game.add_hand(hand2, 'IP')
        self.assertEqual(game.IP_hand, hand2)
        self.assertNotIn(Card.new('Qc'), game.deck.cards)
        self.assertNotIn(Card.new('Jh'), game.deck.cards)

        game.add_community_card(Card.new('2d'))
        game.add_community_card(Card.new('7h'))
        game.add_community_card(Card.new('Ts'))
        game.add_community_card(Card.new('Jd'))
        game.add_community_card(Card.new('Ac'))
        self.assertEqual(len(game.community_cards), 5)
        self.assertNotIn(Card.new('2d'), game.deck.cards)
        self.assertNotIn(Card.new('7h'), game.deck.cards)
        self.assertNotIn(Card.new('Ts'), game.deck.cards)
        self.assertNotIn(Card.new('Jd'), game.deck.cards)
        self.assertNotIn(Card.new('Ac'), game.deck.cards)
        winner = game.evaluate()
        self.assertEqual(winner, 'OOP')  # OOP has a better hand with Ace pair

        


