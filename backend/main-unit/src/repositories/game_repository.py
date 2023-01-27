import os
from datetime import datetime
from typing import List

from pymongo import MongoClient

from misc.tools import async_print
from models.game_models import GameModel
from models.leaderboard_models import Leaderboard, TeamScore

USERNAME = os.getenv('MONGO_USERNAME')
PASSWORD = os.getenv('MONGO_PASSWORD')

MONGO_URI = f"mongodb://{USERNAME}:{PASSWORD}@database:27017"
MONGO_DB = "interactieve-palen"


class GameRepository:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)

        self.db = self.client[MONGO_DB]

    def get_games(self) -> List[GameModel]:
        games = self.db.games.find()
        return [GameModel(**game) for game in games]

    def get_leaderboard(self, game: str):
        scores_for_game = self.db.scores.find({"game": game})

        daily = []
        alltime = []

        today = datetime.today()

        for score in scores_for_game:
            alltime.append(TeamScore(team_name=score["team_name"], score=score["score"]))

            score_date = score["date"]

            if score_date.year == today.year and score_date.month == today.month and score_date.day == today.day:
                daily.append(TeamScore(team_name=score["team_name"], score=score["score"]))

        daily = sorted(daily, key=lambda x: x.score, reverse=True)
        alltime = sorted(alltime, key=lambda x: x.score, reverse=True)

        # limit to top 5
        daily = daily[:5]
        alltime = alltime[:5]

        return Leaderboard(game=game, daily=daily, alltime=alltime)

    def save_score(self, game: str, difficulty: str, team_name: str, score: int):
        self.db.scores.insert_one({"game": game,
                                   "difficulty": difficulty,
                                   "team_name": team_name,
                                   "score": score,
                                   "date": datetime.now()
                                   })

        # commit to db
