from src.tree.node import Node
from src.game.gamestate import GameState
from src.tree.id import create_ids, get_hand_from_id


class TreeBuilder:
    def __init__(self, oop_range, ip_range):
        self.oop_range = oop_range
        self.ip_range = ip_range
        self.root = Node()

    def create_root_node(self, OOP_stack, IP_stack, OOP_contribution, IP_contribution, pot):
        root = Node()

        # Create unique IDs for all combinations of player hands in their ranges
        ids = create_ids(self.oop_range, self.ip_range)
        for hand_id in ids:

            # determine player
            if hand_id.startswith("OOP"):
                player = 'OOP'
            else:
                player = 'IP'
            
            # find correct opponent range
            if player == 'OOP':
                opponent_range = self.ip_range
            else:
                opponent_range = self.oop_range

            # reconstruct hand from id
            hand = get_hand_from_id(hand_id)

            # create gamestate for this hand at root node
            gamestate = GameState(player, hand, opponent_range)
            if player == 'OOP':
                gamestate.player_stack = OOP_stack
                gamestate.player_contribution = OOP_contribution
                gamestate.opponent_stack = IP_stack
                gamestate.opponent_contribution = IP_contribution
            else:
                gamestate.player_stack = IP_stack
                gamestate.player_contribution = IP_contribution
                gamestate.opponent_stack = OOP_stack
                gamestate.opponent_contribution = OOP_contribution

            # add the new state to the node's states dictionary
            root.states[hand_id] = gamestate
        
        return root

        





            
        