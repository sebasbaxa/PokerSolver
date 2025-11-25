from treys import Card

def create_ids(oop_range, ip_range):
    # Create unique IDs for all combinations of player hands in their ranges
    ids = []

    for oop_hand in oop_range.get_hands():
        for ip_hand in ip_range.get_hands():
            # Create a unique ID based on hand representations
            if oop_hand == ip_hand:
                continue  # Skip if both players have the same hand

            hand_id = "OOP{}/IP{}".format(id_hand(oop_hand), id_hand(ip_hand))
            ids.append(hand_id)
    return ids

def id_hand(hand):
    # Create a unique ID for a single hand
    output = ""
    for card in hand.cards:
        output += Card.int_to_str(card)
    return output