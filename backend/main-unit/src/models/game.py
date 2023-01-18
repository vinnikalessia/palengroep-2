from typing import List

from pydantic import BaseModel


class Game(BaseModel):
    name: str
    description: str
    players: str
    num_teams: int


class GamesResponse(BaseModel):
    games: List[Game]


