from src.game.gamestate import GameState
from src.game.player_range import PlayerRange

# Node will cointain a seperate gamestate for hand in a players range and for each node in the gametree

class Node:
    def __init__(self, turn, state, street, stacks, contributions, pot):
        # we will have a gamestate for each possible combination of player hand at this node
        # each hand compination will be assinged an id which maps to a gamestate
        # the id will a int that represents the position and hand so they are unique
        self.states = {}

        self.turn = turn # 'OOP' or 'IP'
        self.street = street # 'flop', 'turn', 'river'
        self.state = state # 'action 'allin' 'fold' or 'showdown
        self.raise_count = 0

        self.stacks = stacks  # {'OOP': int, 'IP': int}
        self.contributions = contributions  # {'OOP': int, 'IP': int}
        self.pot = pot
        self.children = []  # child nodes [0 = fold, 1 = call/check, 2 = raise]