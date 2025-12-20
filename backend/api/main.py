from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import ranges
from api.routes import game
from api.routes import solver

app = FastAPI(title="Poker Solver API", version="1.0.0")

app.include_router(ranges.router)
app.include_router(game.router)
app.include_router(solver.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Poker Solver API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}