from src.game.player_range import PlayerRange



def select_ranges():
    oop_range = PlayerRange('OOP')
    ip_range = PlayerRange('IP')

    print("Select hands for OOP player (enter done when done):")
    while True:
        hand_input = input("Enter hand (e.g., 'AA', 'KQs', 'JTo'): ")
        if hand_input.lower() == 'done':
            break
        elif len(hand_input) == 2 and hand_input[0] == hand_input[1]:
            oop_range.add_pocket_pair(hand_input[0])
        elif len(hand_input) == 3 and hand_input[2] == 's':
            oop_range.add_suited_cards(hand_input[0], hand_input[1])
        elif len(hand_input) == 3 and hand_input[2] == 'o':
            oop_range.add_offsuit_cards(hand_input[0], hand_input[1])
        else:
            print("Invalid input. Please try again.")
    
    print("Select hands for IP player (enter done when done):")
    while True:
        hand_input = input("Enter hand (e.g., 'AA', 'KQs', 'JTo'): ")
        if hand_input.lower() == 'done':
            break
        elif len(hand_input) == 2 and hand_input[0] == hand_input[1]:
            ip_range.add_pocket_pair(hand_input[0])
        elif len(hand_input) == 3 and hand_input[2] == 's':
            ip_range.add_suited_cards(hand_input[0], hand_input[1])
        elif len(hand_input) == 3 and hand_input[2] == 'o':
            ip_range.add_offsuit_cards(hand_input[0], hand_input[1])
        else:
            print("Invalid input. Please try again.")
    
    return {'OOP': oop_range, 'IP': ip_range}
    
