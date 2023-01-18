from typing import List

from pydantic import BaseModel


class SetupGamePayload(BaseModel):
    game: str
    difficulty: str
    teamNames: List[str]
    duration: int
