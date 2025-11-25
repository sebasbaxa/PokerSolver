from src.game.gamestate import GameState
from src.game.player_range import PlayerRange

# Node will cointain a seperate gamestate for hand in a players range and for each node in the gametree

class Node:
    def __init__(self):
        # we will have a gamestate for each possible combination of player hand at this node
        # each hand compination will be assinged an id which maps to a gamestate
        # the id will a int that represents the position and hand so they are unique
        self.states = {}

        self.turn = None # 'OOP' or 'IP'
        self.regret = {"call":0, "raise":0, "fold":0}
        self.strategy = {"call":0, "raise":0, "fold":0}
        self.ev = {"call":0, "raise":0, "fold":0}

