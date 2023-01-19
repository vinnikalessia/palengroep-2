from typing import List

from pydantic import BaseModel


class TeamScore(BaseModel):
    team_name: str
    score: int


class Leaderboard(BaseModel):
    game: str
    difficulty: str
    daily: List[TeamScore]
    alltime: List[TeamScore]


class LeaderboardResponse(BaseModel):
    leaderboard: Leaderboard
