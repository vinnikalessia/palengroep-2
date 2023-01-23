from typing import List

from game.game import Game
from game.game_thread import GameThread
from misc.queue import MessageQueue
from misc.queue.item import QueueItem
from misc.queue.pole_action import PoleActionQueueItem
from models.game_models import GameModel, GameStatusResponse, GameConfigModel
from models.leaderboard_models import LeaderboardResponse
from repositories.games import GameRepository


class GameService:
    def __init__(self, game_repository: GameRepository, client_queue: MessageQueue):
        self.game_repository = game_repository
        self.game_process = None
        self.socket_manager = None
        self.mqtt_client = None

        self.client_queue = client_queue

        self.socket_manager = None

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
        self.game_process = GameThread(game_config=game_setup,
                                       socket_manager=self.socket_manager,
                                       mqtt_client=self.mqtt_client,
                                       client_queue=self.client_queue)
        self.game_process.start()
        return GameStatusResponse(game=game_setup.game, teams=game_setup.teamNames, duration=game_setup.duration,
                                  difficulty=game_setup.difficulty, status="starting")

    def start_game(self):
        self.client_queue.put_nowait(QueueItem("general", "start"))

    def stop_game(self):
        self.game_process.stop()
        # self.game_process.join()
        self.game_process = None

    def pause_game(self):
        self.client_queue.put_nowait(QueueItem("general", "pause"))

    def resume_game(self):
        self.client_queue.put_nowait(QueueItem("general", "resume"))

    def handle_pole_action(self, pole_id: str, action: str):
        self.client_queue.put_nowait(PoleActionQueueItem(pole_id, action))
