from treys import Card
from src.core.hand import Hand

def create_ids(oop_range, ip_range) -> list:
    # Create unique IDs for all of the hands in each players range
    ids = []

    for oop_hand in oop_range.get_hands():
        ids.append("OOP"+ str(oop_hand))

    for ip_hand in ip_range.get_hands():
        ids.append("IP"+ str(ip_hand))
    
    return ids

def get_hand_from_id(hand_id) -> Hand:
    # Reconstruct a Hand object from its unique ID
    cards = []
    if hand_id[0] == 'O':
        hand_id = hand_id[3:]  # Remove "OOP" prefix
    elif hand_id[0] == 'I':
        hand_id = hand_id[2:]  # Remove "IP" prefix
    else:
        raise ValueError("Invalid hand ID format.")

    for i in range(0, len(hand_id), 2):
        card_str = hand_id[i:i+2]
        card_int = Card.new(card_str)
        cards.append(card_int)
    
    return Hand(cards)