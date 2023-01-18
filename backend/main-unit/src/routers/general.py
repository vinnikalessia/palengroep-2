from typing import List

from fastapi import APIRouter
from starlette.responses import RedirectResponse

from models.game import Game, GamesResponse
from repositories.games import GameRepository
from services.games import GameService

router = APIRouter(tags=['global'])
game_service = GameService(game_repository=GameRepository())


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@router.get("/games", description="Get all games")
async def get_games() -> GamesResponse:
    return GamesResponse(games=game_service.get_games())
