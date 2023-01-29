from typing import List

from game.game import GameStatus
from game.game_thread import GameThread
from misc.queue import MessageQueue
from misc.queue.item import QueueItem
from misc.queue.pole_action import PoleActionQueueItem
from misc.tools import async_print
from models.game_models import GameModel, GameStatusResponse, GameConfigModel, CurrentGameStatus
from models.leaderboard_models import LeaderboardResponse
from repositories.game_repository import GameRepository


class GameService:
    def __init__(self, game_repository: GameRepository, client_queue: MessageQueue):
        self.game_repository = game_repository
        self.game_process: GameThread = None
        self.mqtt_client = None

        self.last_game_config = None

        self.client_queue = client_queue

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def get_games(self) -> List[GameModel]:
        return self.game_repository.get_games()

    def get_leaderboard(self, game: str) -> LeaderboardResponse:
        return self.game_repository.get_leaderboard(game)

    def get_score(self):
        return self.game_process.get_score()

    def get_current_game_status(self):
        if self.game_process is None:
            return CurrentGameStatus(
                game="",
                difficulty="",
                scores={},
                elapsed_time=0,
                total_duration=0,
                status=GameStatus.NONE.value

            )
        return self.game_process.get_game_status()

    def setup_game(self, game_setup: GameConfigModel) -> GameStatusResponse:
        if self.game_process is not None:
            self.game_process.stop()
        self.game_process = None
        self.last_game_config = game_setup
        self.game_process = GameThread(game_config=game_setup,
                                       mqtt_client=self.mqtt_client,
                                       client_queue=self.client_queue)
        self.game_process.start()
        return GameStatusResponse(game=game_setup.game, teams=game_setup.teamNames, duration=game_setup.duration,
                                  difficulty=game_setup.difficulty, status="starting")

    def start_game(self):
        async_print("starting game")

        if self.game_process is None:
            return "no game prepared"
        else:
            if self.game_process.game.finished or self.game_process.game.stopped:
                self.setup_game(self.last_game_config)

        if self.game_process is not None and self.game_process.is_alive():
            self.client_queue.put_nowait(QueueItem("general", "start"))
        else:
            self.setup_game(self.last_game_config)
            self.client_queue.put_nowait(QueueItem("general", "start"))

    def stop_game(self):
        if self.game_process is not None and self.game_process.is_alive():
            self.client_queue.put_nowait(QueueItem("general", "stop"))
        else:
            async_print("no game prepared")

    def pause_game(self):
        if self.game_process is not None and self.game_process.is_alive():
            self.client_queue.put_nowait(QueueItem("general", "pause"))
        else:
            async_print("no game running")

    def resume_game(self):
        if self.game_process is not None and self.game_process.is_alive():
            self.client_queue.put_nowait(QueueItem("general", "resume"))
        else:
            async_print("no game running")

    def handle_pole_alive(self, pole_id: str):
        if self.game_process is not None:
            self.game_process.add_alive_esp32(pole_id)

        async_print("pole alive: " + pole_id)

    def handle_pole_action(self, pole_id: str, action: str):
        self.client_queue.put_nowait(PoleActionQueueItem(pole_id, action))
