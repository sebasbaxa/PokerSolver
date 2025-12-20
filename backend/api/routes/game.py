from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from src.game.gamestate import GameState
from src.core.deck import Card


router = APIRouter(prefix="/api/game", tags=["game"])


class GameSetupRequest(BaseModel):
    oop_stack: int = Field(..., gt=0, description="Out of position player's stack size")
    ip_stack: int = Field(..., gt=0, description="In position player's stack size")
    pot: int = Field(..., ge=0, description="Initial pot size")
    flop: List[str] = Field(..., description="List of cards on the flop")

class GameSetupResponse(BaseModel):
    message: str
    oop_stack: int
    ip_stack: int
    pot: int
    flop: List[str]


@router.post("/setup")
async def setup_game(request: GameSetupRequest):
    
    try:
        

        return GameSetupResponse(
            message="Game setup successful",
            oop_stack=request.oop_stack,
            ip_stack=request.ip_stack,
            pot=request.pot,
            flop=request.flop
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
