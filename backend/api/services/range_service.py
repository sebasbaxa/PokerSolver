from src.game.player_range import PlayerRange

# func that takes in hand strings and returns a PlayerRange

def parse_hand_range(range_list: list[str], position: str) -> PlayerRange:
    player_range = PlayerRange(position)
    for hand_str in range_list:
        if len(hand_str) == 2:  # Pocket pair
            rank = hand_str[0]
            # validate rank
            if rank not in '123456789TJQKA':
                raise ValueError(f"Invalid rank in hand format: {hand_str}")
            
            if hand_str[0] != hand_str[1]:
                raise ValueError(f"Invalid pocket pair format: {hand_str}")
            
            player_range.add_pocket_pair(rank)
        elif len(hand_str) == 3:
            rank1 = hand_str[0]
            rank2 = hand_str[1]
            # validating ranks
            if rank1 not in '123456789TJQKA' or rank2 not in '123456789TJQKA':
                raise ValueError(f"Invalid rank in hand format: {hand_str}")
            
            # parsing and validating suits
            suit_indicator = hand_str[2]
            if suit_indicator == 's':  # Suited
                player_range.add_suited_cards(rank1, rank2)
            elif suit_indicator == 'o':  # Offsuit
                player_range.add_offsuit_cards(rank1, rank2)
            else:
                raise ValueError(f"Invalid hand format: {hand_str}")
        else:
            raise ValueError(f"Invalid hand format: {hand_str}")
        
    return player_range