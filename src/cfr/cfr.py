from typing import Any
from src.cfr.winrates import calculate_winrates
from src.tree.node import Node

class CFRSolver:
    def __init__(self, root: Node):
        self.root = root
        self.winrates = calculate_winrates(self.root)

    def calc_values(self, node: Node) -> None:

        # calculate terminal node values
        if node.state == 'showdown':
            for hand_id, gamestate in node.states.items():
                winrate_info = self.winrates[hand_id]
                wins = winrate_info['wins']
                ties = winrate_info['ties']
                total = winrate_info['total']
                winrate = wins / total if total > 0 else 0
                tierate = ties / total if total > 0 else 0
                lossrate = 1 - winrate - tierate
                value = (winrate * node.pot) + (tierate * node.pot * 0.5) - (lossrate * node.pot)
                gamestate.value = value
            
        elif node.state == 'fold':
            folder = 'IP' if node.turn == 'IP' else 'OOP'  # the player who folded is opposite of node.turn
            for hand_id, gamestate in node.states.items():
                if gamestate.player == folder:
                    gamestate.value = 0 # folder gets nothing
                else:
                    gamestate.value = node.pot  # non-folder gets the pot
        
        else:
            if len(node.children) < 3:
                print(node.children)
                raise ValueError("Node must have 3 children to calculate values.")
            for action, child in node.children.items():
                self.calc_values(child)
            
            for hand_id, gamestate in node.states.items():
                for action, child in node.children.items():
                    child_gamestate = child.states[hand_id]
                    gamestate.evs[action] = child_gamestate.value
                # calculate expected value based on current strategy
                ev = 0.0
                for action, prob in gamestate.strategy.items():
                    ev += prob * gamestate.evs[action]
                gamestate.value = ev
                # calculate regrets
                for action in gamestate.strategy.keys():
                    regret = gamestate.evs[action] - gamestate.value
                    gamestate.regret[action] = regret

    def recalc_strategies(self, node: Node) -> None:
        if node.state == 'showdown' or node.state == 'fold':
            return
        
        for hand_id, gamestate in node.states.items():
            # calculate positive regrets
            positive_regrets = {action: max(regret, 0) for action, regret in gamestate.regret.items()}
            total_positive_regret = sum(positive_regrets.values())
            if total_positive_regret > 0:
                for action in gamestate.strategy.keys():
                    gamestate.strategy[action] = positive_regrets[action] / total_positive_regret
            else:
                num_actions = len(gamestate.strategy)
                for action in gamestate.strategy.keys():
                    gamestate.strategy[action] = 1.0 / num_actions
        
        for child in node.children.values():
            self.recalc_strategies(child)