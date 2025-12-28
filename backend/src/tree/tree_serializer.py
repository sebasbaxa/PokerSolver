"""
Tree serialization utilities for converting Node objects to JSON-serializable format.
"""
from src.tree.node import Node
from src.core.id import get_hand_from_id
from typing import List, Dict, Any


def get_card_string_from_hand_id(hand_id: str) -> str:
    """Extract card string from hand ID (remove position prefix)."""
    if hand_id.startswith("OOP"):
        return hand_id[3:]
    elif hand_id.startswith("IP"):
        return hand_id[2:]
    return hand_id


def serialize_full_tree(node: Node, path: str = "root") -> Dict[str, Any]:
    """
    Recursively serialize the entire game tree.
    
    Args:
        node: The Node object to serialize
        path: The action path to reach this node (e.g., "root->call->raise")
    
    Returns:
        Dictionary containing full tree data with nested children
    """
    # Extract strategies for both players
    oop_strategies = []
    ip_strategies = []
    
    for hand_id, gamestate in node.states.items():
        hand_str = get_card_string_from_hand_id(hand_id)
        strategy = {
            'hand': hand_str,
            'fold': gamestate.strategy.get('fold', 0.0),
            'call': gamestate.strategy.get('call', 0.0),
            'raise': gamestate.strategy.get('raise', 0.0),
            'ev': gamestate.value
        }
        
        if gamestate.player == 'OOP':
            oop_strategies.append(strategy)
        else:
            ip_strategies.append(strategy)
    
    # Determine if this is a terminal node
    is_terminal = node.state in ['fold', 'showdown']
    
    # Recursively serialize children
    children_data = {}
    if not is_terminal:
        for action, child_node in node.children.items():
            child_path = f"{path}->{action}"
            children_data[action] = serialize_full_tree(child_node, child_path)
    
    return {
        'path': path,
        'turn': node.turn,
        'street': node.street,
        'state': node.state,
        'pot': node.pot,
        'stacks': node.stacks,
        'contributions': node.contributions,
        'children': children_data,
        'oop_strategy': oop_strategies,
        'ip_strategy': ip_strategies,
        'isTerminal': is_terminal
    }
