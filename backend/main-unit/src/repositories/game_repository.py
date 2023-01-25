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
MONGO_DB = "datastore"


class GameRepository:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)

        self.db = self.client[MONGO_DB]

    def get_games(self) -> List[GameModel]:
        games = self.db.games.find()
        return [GameModel(**game) for game in games]

    def get_leaderboard(self, game: str, difficulty: str):
        scores_for_game = self.db.scores.find({"game": game, "difficulty": difficulty})

        daily = []
        alltime = []

        today = datetime.today()

        for score in scores_for_game:
            alltime.append(TeamScore(team_name=score["team_name"], score=score["score"]))

            score_date = score["date"]

            if score_date.year == today.year and score_date.month == today.month and score_date.day == today.day:
                daily.append(TeamScore(team_name=score["team_name"], score=score["score"]))

        daily = sorted(daily, key=lambda x: x.scores, reverse=True)
        alltime = sorted(alltime, key=lambda x: x.scores, reverse=True)

        # limit to top 10
        daily = daily[:10]
        alltime = alltime[:10]

        return Leaderboard(game=game, difficulty=difficulty, daily=daily, alltime=alltime)

    def save_score(self, game: str, difficulty: str, team_name: str, score: int):
        insert_result = self.db.scores.insert_one({"game": game,
                                                   "difficulty": difficulty,
                                                   "team_name": team_name,
                                                   "score": score,
                                                   "date": datetime.now()
                                                   })

        # commit to db
