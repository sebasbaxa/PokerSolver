from treys import Card

def get_info() -> dict:
    oop_stack = input("Enter OOP stack size: ")
    ip_stack = input("Enter IP stack size: ")
    preflop = input("Enter preflop amount (each player): ")
    contributions = {'OOP': int(preflop), 'IP': int(preflop)}
    pot = int(preflop) * 2

    flop_cards = input("Enter flop cards (e.g., '2h 7h Th'): ")
    flop = []
    for card_str in flop_cards.split():
        flop.append(Card.new(card_str))
    
    return {
        'stacks': {'OOP': int(oop_stack), 'IP': int(ip_stack)},
        'contributions': contributions,
        'pot': pot,
        'flop': flop
    }



