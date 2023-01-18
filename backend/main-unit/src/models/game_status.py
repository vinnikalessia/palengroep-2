from typing import List

from pydantic import BaseModel, Field


class GameStatusResponse(BaseModel):
    game: str
    teams: List[str] = Field(..., example=["team1", "team2"], description="The names of the teams")
    duration: int
    difficulty: str
    status: str = Field(..., example="starting", description="The status of the game")
