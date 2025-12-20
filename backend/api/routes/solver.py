from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from api.services.solver_service import solve

router = APIRouter(prefix="/api/solver", tags=["solver"])


class SolverRequest(BaseModel):
    iterations: int
    oop_range: List[str]
    ip_range: List[str]
    oop_stack: int
    ip_stack: int
    pot: int
    flop: List[str]
    oop_contribution: int
    ip_contribution: int

class SolverResponse(BaseModel):
    oop_strategy: List[dict]
    ip_strategy: List[dict]
    iterations: int
    message: str
    

@router.post("/solve", response_model=SolverResponse)
async def solve_game(request: SolverRequest):
    # use solver service to solve game 
    try:
        result = solve(
            oop_range=request.oop_range,
            ip_range=request.ip_range,
            oop_stack=request.oop_stack,
            ip_stack=request.ip_stack,
            oop_contribution=request.oop_contribution,
            ip_contribution=request.ip_contribution,
            pot=request.pot,
            iterations=request.iterations,
            flop=request.flop
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver error: {str(e)}")

    return SolverResponse(
        oop_strategy=result['oop_strategy'],
        ip_strategy=result['ip_strategy'],
        iterations=result['iterations'],
        message="Game solved successfully",
    )
