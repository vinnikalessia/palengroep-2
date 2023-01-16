from pydantic import BaseModel


class SetupModel(BaseModel):
    game: str
    difficulty: str
    teamNames: list
    duration: int
