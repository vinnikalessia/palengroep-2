from typing import List

from models.game import Game
from models.leaderboard import Leaderboard
from models.team_score import TeamScore


class GameRepository:

    def get_games(self) -> List[Game]:
        return [
            Game(
                name="Red/Blue",
                description="bla bla bla bla bla",
                players="minimum 2",
                num_teams=2,
            ),
            Game(
                name="Zen",
                description="bla bla bla bla bla",
                players="minimum 2",
                num_teams=1,
            ),
            Game(
                name="Simon Says",
                description="bla bla bla bla bla",
                players="minimum 2",
                num_teams=1,
            ),
        ]

    def get_leaderboard(self, game: str, difficulty: str):
        return Leaderboard(
            game=game,
            difficulty=difficulty,
            daily=[
                TeamScore(team_name="Team 1", score=100),
                TeamScore(team_name="Team 1", score=99),
                TeamScore(team_name="Team 1", score=50),
                TeamScore(team_name="Team 1", score=25),
            ],
            alltime=[
                TeamScore(team_name="Team 1", score=100),
                TeamScore(team_name="Team 1", score=99),
                TeamScore(team_name="Team 1", score=50),
                TeamScore(team_name="Team 1", score=25),
            ]
        )

    def get_score(self):
        return