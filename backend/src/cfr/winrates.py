from src.tree.node import Node
from treys import Evaluator
from src.game.player_range import PlayerRange
import random
import copy
from multiprocessing import Pool, cpu_count
import itertools



def evaluate_matchup(args):
    ip_hand, oop_hand, flop, deck_cards = args
    evaluator = Evaluator()
    results = {'IP_wins': 0, 'OOP_wins': 0, 'ties': 0}
    
    valid_cards = [card for card in deck_cards 
                   if card not in ip_hand.cards and card not in oop_hand.cards]
    
    for turn in valid_cards:
        runout = flop + [turn]
        for river in [card for card in valid_cards if card != turn]:
            full_runout = runout + [river]
            
            ip_score = evaluator.evaluate(ip_hand.cards, full_runout)
            oop_score = evaluator.evaluate(oop_hand.cards, full_runout)
            
            if ip_score < oop_score:
                results['IP_wins'] += 1
            elif oop_score < ip_score:
                results['OOP_wins'] += 1
            else:
                results['ties'] += 1
    
    return (str(ip_hand), str(oop_hand), results)

def create_win_cache_parallel(IPrange: PlayerRange, OOPrange: PlayerRange, root: Node) -> dict:
    gamestate = root.states[next(iter(root.states))]
    flop = copy.deepcopy(gamestate.community_cards)
    deck_cards = gamestate.deck.cards
    
    # Filter valid hands
    valid_ip_hands = [h for h in IPrange.get_hands() if not any(c in flop for c in h.cards)]
    valid_oop_hands = [h for h in OOPrange.get_hands() if not any(c in flop for c in h.cards)]
    
    # Create matchup arguments
    matchups = [(ip_hand, oop_hand, flop, deck_cards) 
                for ip_hand in valid_ip_hands 
                for oop_hand in valid_oop_hands]
    
    # Process in parallel
    with Pool(cpu_count()) as pool:
        results = pool.map(evaluate_matchup, matchups)
    
    # Build cache
    win_cache = {}
    for ip_str, oop_str, res in results:
        ip_key = f"IP{ip_str}"
        oop_key = f"OOP{oop_str}"
        
        if ip_key not in win_cache:
            win_cache[ip_key] = {}
        if oop_key not in win_cache:
            win_cache[oop_key] = {}
            
        win_cache[ip_key][oop_key] = res
        win_cache[oop_key][ip_key] = res
    
    return win_cache


def sample_hand_by_reach(node: Node, prefix: str) -> str:
        # generate a hand_id sampled according to reach probabilities

        # collect candidate hand_ids for the player
        hand_ids = [hid for hid in node.states.keys() if hid.startswith(prefix)]
        if not hand_ids:
            raise ValueError(f"No hand_ids for {prefix} at node")

        # get weights from reach, fallback to uniform if all zero/missing
        weights = [node.reach.get(hid, 0.0) for hid in hand_ids]
        if sum(weights) <= 0.0:
            weights = [1.0] * len(hand_ids)

        # sample one hand_id according to reach weights
        return random.choices(hand_ids, weights=weights, k=1)[0]



def create_win_cache(IPrange: PlayerRange, OOPrange: PlayerRange, root: Node) -> dict:
    # create the cache of winrates for all hands in both ranges
    # dict structure:
    # win_cache = {
    #   'IP<hand>': {
    #       'OOP<hand>': {'IP_wins': int, 'OOP_wins': int, 'ties': int},
    #       ...
    #   },
    #   'OOP<hand>': {
    #       'IP<hand>': {'IP_wins': int, 'OOP_wins': int, 'ties': int},
    #       ...
    #   }
    # }

    # Create a cache of winrates for all hands in IP and OOP ranges
    win_cache = {}
    evaluator = Evaluator()
    gamestate = root.states[next(iter(root.states))]
    flop = copy.deepcopy(gamestate.community_cards)


    # every hand in IP's range
    for ip_hand in IPrange.get_hands():
        # check if hand is valid with flop
        if any(card in flop for card in ip_hand.cards):
            continue

        win_cache["IP"+ str(ip_hand)] = {}

        # every hand in OOP's range
        for oop_hand in OOPrange.get_hands():
            # check if hand is valid with flop
            if any(card in flop for card in oop_hand.cards):
                continue

            win_cache["IP"+ str(ip_hand)]["OOP"+ str(oop_hand)] = {'IP_wins':0, 'OOP_wins':0, 'ties':0}
            if "OOP"+ str(oop_hand) not in win_cache:
                win_cache["OOP"+ str(oop_hand)] = {}
            win_cache["OOP"+ str(oop_hand)]["IP"+ str(ip_hand)] = {'IP_wins':0, 'OOP_wins':0, 'ties':0}
            # simulate turn and river
            for turn in [card for card in gamestate.deck.cards if card not in ip_hand.cards and card not in oop_hand.cards]:
                runnout = flop + [turn]
                for river in [card for card in gamestate.deck.cards if card != turn and card not in ip_hand.cards and card not in oop_hand.cards]:
                    full_runnout = runnout + [river]

                    ip_score = evaluator.evaluate(ip_hand.cards, full_runnout)
                    oop_score = evaluator.evaluate(oop_hand.cards, full_runnout)

                    if ip_score < oop_score:
                        win_cache["IP"+ str(ip_hand)]["OOP"+ str(oop_hand)]['IP_wins'] += 1
                        win_cache["OOP"+ str(oop_hand)]["IP"+ str(ip_hand)]['IP_wins'] += 1
                    elif oop_score < ip_score:
                        win_cache["IP"+ str(ip_hand)]["OOP"+ str(oop_hand)]['OOP_wins'] += 1
                        win_cache["OOP"+ str(oop_hand)]["IP"+ str(ip_hand)]['OOP_wins'] += 1
                    else:
                        win_cache["IP"+ str(ip_hand)]["OOP"+ str(oop_hand)]['ties'] += 1
                        win_cache["OOP"+ str(oop_hand)]["IP"+ str(ip_hand)]['ties'] += 1
    return win_cache

                    
            
            
        


    
