from typing import Any
from src.cfr import winrates
from src.cfr.winrates import create_win_cache, sample_hand_by_reach
from src.tree.node import Node
from treys import evaluator
import random


#TODO: compine calc values into one funcion with position parameter reducing code duplication

# Class containing methods to perform CFR calculations
class CFRSolver:
    def __init__(self, root: Node, win_cache: dict) -> None:
        self.root = root
        self.win_cache = win_cache


    #TODO: Combine this function and the calc_OOP_values function to reduce code duplication

    def calc_values(self, node: Node, pos: str) -> None:
        other_pos = 'IP' if pos == 'OOP' else 'OOP'

        def dfs(curr: Node) -> None:
            if curr.state == 'fold':
                for hand_id, gamestate in curr.states.items():
                    if gamestate.player != pos:
                        continue
                    if curr.turn == other_pos:
                        # if other player folded, current player wins the pot
                        gamestate.value = curr.contributions[other_pos]
                    else:
                        # if current player folded, other player wins the pot
                        gamestate.value = -curr.contributions[pos]
                return
            elif curr.state == 'showdown':
                
                for hand_id, gamestate in curr.states.items():
                    if gamestate.player != pos:
                        continue

                    # get winrate
                    win_data = {'wins':0, 'ties':0, 'total':0}  
                    info = self.win_cache.get(hand_id, {})
                    for opp_hand_id, opp_info in info.items():
                        opp_reach = curr.reach.get(opp_hand_id, 0.0)
                        win_data['wins'] += opp_info[f'{pos}_wins'] * opp_reach
                        win_data['ties'] += opp_info['ties'] * opp_reach
                        win_data['total'] += (opp_info['IP_wins'] + opp_info['OOP_wins'] + opp_info['ties']) * opp_reach
                    if win_data['total'] == 0:
                        gamestate.value = 0.0
                    else:
                        gamestate.value = ((win_data['wins'] / win_data['total'] * curr.pot) + (win_data['ties'] / win_data['total']) * (curr.pot / 2)) - curr.contributions[other_pos]
                    
                return
            if curr.turn == pos:
                # current player's turn to act

                for action, child in curr.children.items():
                    dfs(child)
                
                for hand_id, gamestate in curr.states.items():
                    if gamestate.player != pos:
                        continue
                    ev = 0.0
                    for action, child in curr.children.items():
                        child_gamestate = child.states[hand_id]
                        gamestate.evs[action] = child_gamestate.value
                        ev += gamestate.strategy[action] * child_gamestate.value
                    gamestate.value = ev
                
                for hand_id, gamestate in curr.states.items():
                    if gamestate.player != pos:
                        continue
                    for action in ['fold', 'call', 'raise']:
                        gamestate.regret[action] += gamestate.evs[action] - gamestate.value
            else:
                # other player's turn to act
                for action, child in curr.children.items():
                    dfs(child)
                
                opp_gamestate = curr.states[sample_hand_by_reach(curr, other_pos)]

                for hand_id, gamestate in curr.states.items():
                    if gamestate.player != pos:
                        continue
                    ev = 0.0
                    for action, child in curr.children.items():
                        child_gamestate = child.states[hand_id]
                        gamestate.evs[action] = child_gamestate.value
                        ev += opp_gamestate.strategy[action] * child_gamestate.value
                    gamestate.value = ev

        dfs(node)



    def calc_strategy(self, node: Node, position: str) -> None:
        if node.state == 'showdown' or node.state == 'fold':
            return
        
        if node.turn != position:
            for child in node.children.values():
                self.calc_strategy(child, position)
            return
        
        for hand_id, gamestate in node.states.items():
            # calculate positive regrets
            if gamestate.player != position:
                continue

            positive_regrets = {action: max(regret, 0) for action, regret in gamestate.regret.items()}
            total_positive_regret = sum(positive_regrets.values())
            if total_positive_regret > 0:
                for action in gamestate.strategy.keys():
                    gamestate.strategy[action] = positive_regrets[action] / total_positive_regret
            else:
                num_actions = len(gamestate.strategy)
                for action in gamestate.strategy.keys():
                    gamestate.strategy[action] = 1.0 / num_actions
            
            for action in gamestate.strategy.keys():
                node.children[action].reach[hand_id] = node.reach.get(hand_id, 0.0) * gamestate.strategy[action]
        
        for child in node.children.values():
            self.calc_strategy(child, position)

    def propagate_reach(self, node: Node) -> None:
        def propagate(curr: Node) -> None:
            if curr.state == 'showdown' or curr.state == 'fold':
                return
            
            for hand_id, gamestate in curr.states.items():
                for action in gamestate.strategy.keys():
                    if action in curr.children:
                        curr.children[action].reach[hand_id] = curr.reach.get(hand_id, 1.0) * gamestate.strategy[action]
            
            for child in curr.children.values():
                propagate(child)
    
        propagate(node)
            