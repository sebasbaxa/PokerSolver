from src.game.gamestate import GameState
from src.game.player_range import PlayerRange

#

class Node:
    def __init__(self, turn, state, street, stacks, contributions, pot):
        # Nodes cotain a mapping of every hand_id to their gamestate
        self.states = {}

        # mapping of hand_id to reach probability
        # dict structure: reach = { '<hand_id>': float }
        self.reach: dict[str, float] = {}

        self.turn = turn # 'OOP' or 'IP'
        self.street = street # 'flop', 'turn', 'river'
        self.state = state # 'action 'allin' 'fold' or 'showdown

        # count of raises on this street at this node
        self.raise_count = 0

        self.stacks = stacks  # {'OOP': int, 'IP': int}
        self.contributions = contributions  # {'OOP': int, 'IP': int}
        self.pot = pot
        self.children = {} # action:str -> Node | to be populated later
    
    def __repr__(self) -> str:
        output =  f"Node: turn={self.turn}, street={self.street}, state={self.state}, pot={self.pot}, stacks={self.stacks}, contributions={self.contributions}\n"
        output += "\n States:\n"
        for state_id, gamestate in self.states.items():
            if state_id.startswith(self.turn):
                output += f"  State ID: {state_id}, Gamestate: {gamestate}\n"
        return output