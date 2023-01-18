from typing import List

from models.game import Game
from models.leaderboard import Leaderboard, LeaderboardResponse
from models.game_status import GameStatusResponse
from models.setup_game import SetupGamePayload
from repositories.games import GameRepository


class GameService:
    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def get_games(self) -> List[Game]:
        return self.game_repository.get_games()

    def get_leaderboard(self, game: str, difficulty: str) -> LeaderboardResponse:
        return self.game_repository.get_leaderboard(game, difficulty)

    def get_score(self):
        return self.game_repository.get_score()

    def start_game(self, game_setup: SetupGamePayload) -> GameStatusResponse:
        game = game_setup.game
        difficulty = game_setup.difficulty
        team_names = game_setup.teamNames
        duration = game_setup.duration

        return GameStatusResponse(game=game, teams=team_names, duration=duration, difficulty=difficulty,
                                  status="starting")
