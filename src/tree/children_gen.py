# Function to create children for a node in the game tree
# Children will be fold, call/check, raise nodes
from src.tree.node import Node

def create_fold_child(node) -> Node:
    fold_child = Node('IP' if node.turn == 'IP' else 'OOP', 'terminal', 
                      node.stacks, node.contributions, node.pot)
    return fold_child

def create_call_child(node) -> Node:
    
    if node.contributions[node.turn] == node.contributions['OOP' if node.turn == 'IP' else 'IP']:
        # Check case
        call_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'action', 
                           node.stacks, node.contributions, node.pot)
    else:
        # Call case
        call_amount = node.contributions['OOP' if node.turn == 'IP' else 'IP'] - node.contributions[node.turn]
        new_contributions = node.contributions.copy()
        new_contributions[node.turn] += call_amount
        new_stacks = node.stacks.copy()
        new_stacks[node.turn] -= call_amount
        new_pot = node.pot + call_amount

        call_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'action',
                           new_stacks, new_contributions, new_pot)
        
    return call_child

def create_raise_child(node, raise_amount) -> Node:
    if node.raise_count < 2:  # Limit to 2 raises per betting round
        raise_amount = node.stacks[node.turn] // 2  # Standard raise amount (half the stack)

        # New parameters after raise 
        new_pot = node.pot + raise_amount
        new_contributions = node.contributions.copy()
        new_contributions[node.turn] += raise_amount
        new_stacks = node.stacks.copy()
        new_stacks[node.turn] -= raise_amount

        raise_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'action', 
                        new_stacks, new_contributions, new_pot)
        raise_child.raise_count = node.raise_count + 1
    else:
        raise_child = create_call_child(node)  # If raise limit reached, default to call/check child
        raise_child.raise_count = 0 # reset raise count

    return raise_child