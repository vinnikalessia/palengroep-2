from typing import List, Dict

from pydantic import BaseModel, Field


class GameModel(BaseModel):
    name: str
    display_name: str
    description: str
    players: str
    num_teams: int


class GamesResponse(BaseModel):
    games: List[GameModel]


class GameStatusResponse(BaseModel):
    game: str
    teams: List[str] = Field(..., example=["team1", "team2"], description="The names of the teams")
    duration: int = Field(..., example=15, description="The duration of the game in seconds")
    difficulty: str = Field(..., example="traag", description="The difficulty of the game")
    status: str = Field(..., example="starting", description="The status of the game")


class CurrentGameStatus(BaseModel):
    game: str
    status: str
    elapsed_time: int
    total_duration: int
    difficulty: str
    scores: Dict[str, int] = Field(..., example={"team1": 100, "team2": 50},
                                   description="The score of the game per team")

    def __init__(self, game, difficulty, status, scores, elapsed_time, total_duration):
        super().__init__(game=game, difficulty=difficulty, status=status, scores=scores, elapsed_time=elapsed_time,
                         total_duration=total_duration)


class GameScore(BaseModel):
    game: str = Field(..., example="redblue", description="The name of the game")
    difficulty: str = Field(..., example="traag", description="The difficulty of the game")
    scores: Dict[str, int] = Field(..., example={"team1": 100, "team2": 50},
                                   description="The score of the game per team")


class GameConfigModel(BaseModel):
    game: str = Field(..., example="redblue", description="The name of the game")
    difficulty: str = Field(..., example="traag", description="The difficulty of the game")
    teamNames: List[str] = Field(..., example=["team1", "team2"], description="The names of the teams")
    duration: int = Field(..., example=15, description="The duration of the game in seconds")
