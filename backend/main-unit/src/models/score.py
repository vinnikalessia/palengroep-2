from typing import Dict

from pydantic import BaseModel, Field


class GameScore(BaseModel):
    game: str
    difficulty: str
    score: Dict[str, int] = Field(..., example={"team1": 100, "team2": 50},
                                  description="The score of the game per team")


