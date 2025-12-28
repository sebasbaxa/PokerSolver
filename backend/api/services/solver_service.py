from src.cfr.cfr import CFRSolver
from src.cfr.winrates import create_win_cache, create_win_cache_parallel
from src.tree.tree_builder import TreeBuilder
from src.tree.tree_serializer import serialize_full_tree
from api.services.range_service import parse_hand_range
from src.core.id import get_hand_from_id
from treys import Card
from typing import List


# takes in ranges, stacks, contributions, pot size, number of iterations from API and returns solved game tree
def solve(oop_range: List[str], ip_range: List[str], oop_stack: int, ip_stack: int, oop_contribution: int, ip_contribution: int, pot: int, flop: List[str]) -> dict:
    oop_player_range = parse_hand_range(oop_range, 'OOP')
    ip_player_range = parse_hand_range(ip_range, 'IP')

    ranges = {'OOP': oop_player_range, 'IP': ip_player_range}
    stacks = {'OOP': oop_stack, 'IP': ip_stack}
    contributions = {'OOP': oop_contribution, 'IP': ip_contribution}


    # reconstrucing flop cards
    flop_cards = [Card.new(card_str) for card_str in flop]

    # generate game tree
    tree_builder = TreeBuilder(ranges, stacks, contributions, pot, flop_cards)

    print("generating game tree...")
    tree_builder.generate_tree()
    root_node = tree_builder.root
    print("game tree generated.")

    print("creating win cache...")
    win_cache = create_win_cache_parallel(ip_player_range, oop_player_range, root_node)
    print("win cache created.")
    cfr_solver = CFRSolver(root_node, win_cache)

    # solving game tree with CFR
    print('solving...')

    # TODO: can create a way to pass in number of iterations from API later
    for _ in range(200):
        print(f'Iteration {_+1}/200') 
        cfr_solver.calc_strategy(root_node, 'IP')
        cfr_solver.calc_strategy(root_node, 'OOP')
        cfr_solver.propagate_reach(root_node)
        cfr_solver.calc_values(root_node, 'OOP')
        cfr_solver.calc_values(root_node, 'IP')


    # extracting strategies to return
    oop_strategies = []
    ip_strategies = []

    for hand_id, gamestate in root_node.states.items():
        hand = get_card_from_hand_id(hand_id)
        strategy = {
            'hand': hand,
            'fold': gamestate.strategy.get('fold', 0.0),
            'call': gamestate.strategy.get('call', 0.0),
            'raise': gamestate.strategy.get('raise', 0.0),
            'ev': gamestate.value
        }

        if gamestate.player == 'OOP':
            oop_strategies.append(strategy)
        else:
            ip_strategies.append(strategy)
    
    # Serialize the entire game tree
    tree_data = serialize_full_tree(root_node)
    
    return {
        'oop_strategy': oop_strategies,
        'ip_strategy': ip_strategies,
        'tree_data': tree_data,
    }


def get_card_from_hand_id(hand_id: str) -> str:
    if hand_id[0] == 'O':
        hand_id = hand_id[3:]  # remove OOP prefix
    elif hand_id[0] == 'I':
        hand_id = hand_id[2:]  # remove IP prefix

    return hand_id