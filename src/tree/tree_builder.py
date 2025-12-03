from src.tree.node import Node
from src.game.gamestate import GameState
from src.tree.id import create_ids, get_hand_from_id
from src.tree.children_gen import create_fold_child, create_call_child, create_raise_child


class TreeBuilder:
    def __init__(self, ranges, stacks, contributions, pot):
        self.ranges = ranges  # {'OOP': PlayerRange, 'IP': PlayerRange}
        self.stacks = stacks  # {'OOP': int, 'IP': int}
        self.contributions = contributions  # {'OOP': int, 'IP': int}
        self.pot = pot
        self.root = None

    def create_root_node(self) -> Node:
        root = Node('OOP', 'action', 'flop', self.stacks, self.contributions, self.pot)

        # Create unique IDs for all combinations of player hands in their ranges
        ids = create_ids(self.ranges['OOP'], self.ranges['IP'])
        for hand_id in ids:

            # determine player
            if hand_id.startswith("OOP"):
                player = 'OOP'
            else:
                player = 'IP'
            
            # find correct opponent range
            if player == 'OOP':
                opponent_range = self.ranges['IP']
            else:
                opponent_range = self.ranges['OOP']

            # reconstruct hand from id
            hand = get_hand_from_id(hand_id)

            # create gamestate for this hand at root node
            gamestate = GameState(player, hand, opponent_range)

            # add the new state to the node's states dictionary
            root.states[hand_id] = gamestate
        
        return root

    # Generate the full game tree starting from the root node
    def generate_tree(self):
        self.root = self.create_root_node()
        self.recursive_build(self.root)
    
    # recursively build the tree
    def recursive_build(self, node):
        if node.state == 'terminal':
            return
        
        self.create_children(node)
        for child in node.children:
            self.recursive_build(child)

    def create_children(self, node) -> None:

        # dont create any children for terminal nodes
        if node.state == 'terminal':
            return
        
        # Create fold child
        fold_child = create_fold_child(node)
        node.children.append(fold_child)

        # Create call/check child
        call_child = create_call_child(node)
        node.children.append(call_child)

        # Raise child
        raise_child = create_raise_child(node)
        node.children.append(raise_child)