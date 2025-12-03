# Function to create children for a node in the game tree
# Children will be fold, call/check, raise nodes
from src.tree.node import Node
import copy

def create_fold_child(node: Node) -> Node:
    fold_child = Node('IP' if node.turn == 'IP' else 'OOP', 'fold', node.street,
                      node.stacks, node.contributions, node.pot)
    fold_child.states = copy.deepcopy(node.states)  # carry over states
    return fold_child

def create_call_child(node: Node) -> Node:

    if node.state == 'allin':
        # the previous node was allin so this call child is just a showdown node
        call_amount = node.contributions['OOP' if node.turn == 'IP' else 'IP'] - node.contributions[node.turn]
        new_contributions = node.contributions.copy()
        new_contributions[node.turn] += call_amount
        new_stacks = node.stacks.copy()
        new_stacks[node.turn] -= call_amount
        new_pot = node.pot + call_amount
        call_child = Node(node.turn, 'showdown', node.street,
                          new_stacks, new_contributions, new_pot)
        call_child.states = copy.deepcopy(node.states)  # carry over states
        return call_child


    # Check case
    if node.contributions[node.turn] == node.contributions['OOP' if node.turn == 'IP' else 'IP']:

        # IP check logic
        # IP check on last street
        if node.street == 'river' and node.turn == 'IP':
            call_child = Node(node.turn, 'showdown', node.street,
                           node.stacks, node.contributions, node.pot)
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child
        
        # moving streets after IP check
        elif node.turn == 'IP':
            if node.street == 'flop':
                next_street = 'turn'
            elif node.street == 'turn':
                next_street = 'river'
            # Create child node for next street
            call_child = Node('OOP', 'action', next_street,
                           node.stacks, node.contributions, node.pot)
            call_child.raise_count = 0 # reset raise count
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child

        # OOP check logic
        else:
            call_child = Node('IP', 'action', node.street,
                            node.stacks, node.contributions, node.pot)
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child
        
    # Call case
    else:

        # call amount calculation and new parameters
        call_amount = node.contributions['OOP' if node.turn == 'IP' else 'IP'] - node.contributions[node.turn]

        # All in case
        if node.stacks[node.turn] <= call_amount:
            call_amount = node.stacks[node.turn]
            new_contributions = node.contributions.copy()
            new_contributions[node.turn] += call_amount
            new_stacks = node.stacks.copy()
            new_stacks[node.turn] -= call_amount # should be 0
            new_pot = node.pot + call_amount
            call_child = Node(node.turn, 'allin', node.street,
                           new_stacks, new_contributions, new_pot)
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child

        # Normal call case
        new_contributions = node.contributions.copy()
        new_contributions[node.turn] += call_amount
        new_stacks = node.stacks.copy()
        new_stacks[node.turn] -= call_amount
        new_pot = node.pot + call_amount

        # river call logic
        if node.street == 'river':
            call_child = Node(node.turn, 'showdown', node.street,
                           new_stacks, new_contributions, new_pot)
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child

        # IP call logic
        elif node.turn == 'IP':
            if node.street == 'flop':
                next_street = 'turn'
            elif node.street == 'turn':
                next_street = 'river'
            # Create child node for next street
            call_child = Node('OOP', 'action', next_street,
                           new_stacks, new_contributions, new_pot)
            call_child.raise_count = 0 # reset raise count
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child
        
        # OOP call logic
        else:
            call_child = Node('IP', 'action', node.street,
                            new_stacks, new_contributions, new_pot)
            call_child.states = copy.deepcopy(node.states)  # carry over states
            return call_child

def create_raise_child(node: Node) -> Node:

    if node.state == 'allin':
        # cannot raise from allin state, so create call child instead
        raise_child = create_call_child(node)
        return raise_child

    # first raise logic
    if node.raise_count == 0:
        raise_amount = node.pot // 2  # Standard raise amount (half the pot)

        # All in case
        if node.stacks[node.turn] <= raise_amount:
            raise_amount = node.stacks[node.turn]
            new_pot = node.pot + raise_amount
            new_contributions = node.contributions.copy()
            new_contributions[node.turn] += raise_amount
            new_stacks = node.stacks.copy()
            new_stacks[node.turn] -= raise_amount  # should be 0
            raise_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'allin', node.street,
                            new_stacks, new_contributions, new_pot)
            raise_child.raise_count = node.raise_count + 1
            raise_child.states = copy.deepcopy(node.states)  # carry over states
            return raise_child

        # Normal first raise case
        new_pot = node.pot + raise_amount
        new_contributions = node.contributions.copy()
        new_contributions[node.turn] += raise_amount
        new_stacks = node.stacks.copy()
        new_stacks[node.turn] -= raise_amount

        raise_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'action', node.street,
                        new_stacks, new_contributions, new_pot)
        raise_child.states = copy.deepcopy(node.states)  # carry over states
        raise_child.raise_count = node.raise_count + 1
        return raise_child

        # reraise logic
        # TODO: create a way to change max reraises per street and custom reraise and raise amounts
    elif node.raise_count < 2:
        previous_raise = node.contributions['OOP' if node.turn == 'IP' else 'IP'] - node.contributions[node.turn]
        raise_amount = previous_raise * 3  # default to 3x raise

        # All in case
        if node.stacks[node.turn] <= raise_amount:
            raise_amount = node.stacks[node.turn]
            new_pot = node.pot + raise_amount
            new_contributions = node.contributions.copy()
            new_contributions[node.turn] += raise_amount
            new_stacks = node.stacks.copy()
            new_stacks[node.turn] -= raise_amount  # should be 0
            raise_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'allin', node.street,
                            new_stacks, new_contributions, new_pot)
            raise_child.states = copy.deepcopy(node.states)  # carry over states
            raise_child.raise_count = node.raise_count + 1
            return raise_child
        
        # Normal reraise case
        new_pot = node.pot + raise_amount
        new_contributions = node.contributions.copy()
        new_contributions[node.turn] += raise_amount
        new_stacks = node.stacks.copy()
        new_stacks[node.turn] -= raise_amount
        raise_child = Node('IP' if node.turn == 'OOP' else 'OOP', 'action', node.street,
                        new_stacks, new_contributions, new_pot)
        raise_child.states = copy.deepcopy(node.states)  # carry over states
        raise_child.raise_count = node.raise_count + 1
        return raise_child

    # max raises reached logic / resort to call logic
    else:
        # Move to next street after max raise reached

        # we can use default calling logic to create the raise child for IP
        if node.turn == 'IP':
            raise_child = create_call_child(node)
            return raise_child

        # for OOP we need to manually create the next street node
        call_size = node.contributions['IP'] - node.contributions['OOP']
        new_contributions = node.contributions.copy()
        new_contributions['OOP'] += call_size
        new_stacks = node.stacks.copy()
        new_stacks['OOP'] -= call_size
        new_pot = node.pot + call_size

        if node.street == 'flop':
            next_street = 'turn'
        elif node.street == 'turn':
            next_street = 'river'
        else:
            raise_child = Node(node.turn, 'showdown', node.street,
                        new_stacks, new_contributions, new_pot)
            raise_child.states = copy.deepcopy(node.states)  # carry over states
            return raise_child
        
        raise_child = Node('OOP', 'action', next_street,
                        new_stacks, new_contributions, new_pot)    
        raise_child.raise_count = 0 # reset raise count
        raise_child.states = copy.deepcopy(node.states)  # carry over states
    return raise_child