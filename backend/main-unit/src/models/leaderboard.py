from typing import List

from pydantic import BaseModel

from models.team_score import TeamScore


class Leaderboard(BaseModel):
    game: str
    difficulty: str
    daily: List[TeamScore]
    alltime: List[TeamScore]


class LeaderboardResponse(BaseModel):
    leaderboard: Leaderboard
