from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from api.services.range_service import parse_hand_range

router = APIRouter(prefix="/api/ranges", tags=["ranges"])


class RangeResponse(BaseModel):
    player: str
    hands: List[str]
    count: int

class RangeCreateRequest(BaseModel):
    player: str      # "OOP" or "IP"
    hands: List[str] # ["AA", "KQs", "JTo"]

@router.post("/create", response_model=RangeResponse)
def create_range(request: RangeCreateRequest):
    # creating a poker range for a player
    try:
        player_range = parse_hand_range(request.hands, request.player)

        hand_strings = [str(hand) for hand in player_range.get_hands()]

        return RangeResponse(
            player=player_range.id,
            hands=hand_strings,
            count=len(hand_strings)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/presets")
def get_presets():
    # return some preset ranges
    presets = {
        "tight": ["AA", "KK", "QQ", "AKs"],
        "loose": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AQs", "AJs"],
        "balanced": ["AA", "KK", "QQ", "JJ", "AKs", "AQs", "AJs", "KQs"]
    }
    return presets