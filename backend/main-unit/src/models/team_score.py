from pydantic import BaseModel


class TeamScore(BaseModel):
    team_name: str
    score: int
