from src.tree.node import Node
from treys import Evaluator

# Function to calculate the winrates of each hand against the opponent range
def calculate_winrates(node: Node) -> dict:

    winrates = {}
    for hand_id, gamestate in node.states.items():
        if len(gamestate.community_cards) < 3:
            raise ValueError("Community cards must be at least 3 to calculate winrates.")

        evaluator = Evaluator()
        player_wins = 0
        ties = 0
        total = 0

        runnout = gamestate.community_cards.copy()
        for turn in gamestate.deck.cards:
            runnout.append(turn)
            for river in gamestate.deck.cards:
                if river != turn:
                    runnout.append(river)
                    player_score = evaluator.evaluate(gamestate.player_hand.cards, runnout)
                    for opponent_hand in gamestate.opponent_range.get_hands():
                        break_con = False
                        for card in opponent_hand.cards:
                            if card not in gamestate.deck.cards or card == turn or card == river:
                                break_con = True
                                break
                        if break_con:
                            continue
                        opponent_score = evaluator.evaluate(opponent_hand.cards, runnout)
                        total += 1
                        if player_score < opponent_score:
                            player_wins += 1
                        elif player_score == opponent_score:
                            ties += 1
                    runnout.pop()  # remove river
            runnout.pop()  # remove turn
                    
        winrates[hand_id] = {
            'wins': player_wins,
            'ties': ties,
            'total': total,
        }
    return winrates
