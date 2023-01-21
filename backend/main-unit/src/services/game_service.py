from typing import List

from domain.game import Game
from game.game_thread import GameThread
from misc.queue import GameMessageQueue
from misc.queue.items.item import QueueItem
from misc.queue.items.pole_action import PoleActionQueueItem
from models.game_models import GameModel, GameStatusResponse, GameConfigModel
from models.leaderboard_models import LeaderboardResponse
from repositories.games import GameRepository


class GameService:
    def __init__(self, game_repository: GameRepository, msg_queue: GameMessageQueue):
        self.game_repository = game_repository
        self.game_process = None
        self.socket_manager = None
        self.mqtt_client = None
        self.msg_queue = msg_queue

    def set_socket_manager(self, socket_manager):
        self.socket_manager = socket_manager

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def get_games(self) -> List[GameModel]:
        return self.game_repository.get_games()

    def get_leaderboard(self, game: str, difficulty: str) -> LeaderboardResponse:
        return self.game_repository.get_leaderboard(game, difficulty)

    def get_score(self):
        return self.game_repository.get_score()

    def setup_game(self, game_setup: GameConfigModel) -> GameStatusResponse:
        game = Game.from_config(game_setup)

        self.game_process = GameThread(game, self.socket_manager, self.mqtt_client, self.msg_queue)
        # background_tasks.add_task(self.game_process.run)
        return GameStatusResponse(game=game_setup.game, teams=game_setup.teamNames, duration=game_setup.duration,
                                  difficulty=game_setup.difficulty, status="starting")

    def start_game(self):
        self.game_process.start()

    def stop_game(self):
        self.game_process.stop()
        self.game_process.join()
        self.game_process = None

    def pause_game(self):
        self.msg_queue.put(QueueItem("general", "pause"))

    def resume_game(self):
        self.msg_queue.put(QueueItem("general", "resume"))

    def handle_pole_action(self, pole_id: str, action: str):
        self.msg_queue.put(PoleActionQueueItem(pole_id, action))
