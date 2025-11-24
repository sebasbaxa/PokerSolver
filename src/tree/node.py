from src.game.gamestate import GameState
from src.game.player_range import PlayerRange

# Node will cointain a seperate gamestate for hand in a players range and for each node in the gametree

class Node:
    def __init__(self):
        self.gamestate = GameState()
        self.player_ranges = {
            'OOP': PlayerRange('OOP'),
            'IP': PlayerRange('IP')
        }