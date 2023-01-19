import threading
import time
from typing import List

from fastapi_mqtt import FastMQTT

from domain.game import Game
from misc.game_queue import GameMessageQueue, QueueItem
from misc.tools import async_print
from models.game_models import GameModel, GameStatusResponse, GameConfigModel
from models.leaderboard_models import LeaderboardResponse
from repositories.games import GameRepository


class GameProcess(threading.Thread):
    def __init__(self, game: Game, socket_manager, mqtt_client,
                 message_queue: GameMessageQueue):
        self.socket_manager = socket_manager
        self.mqtt_client: FastMQTT = mqtt_client
        self.game = game
        self.message_queue = message_queue
        super().__init__(name="game thread")

    def stop(self):
        self.message_queue.put(QueueItem("general", "stop"))

    def clear_msg_queue(self):
        while not self.message_queue.empty():
            self.message_queue.get_nowait()
            self.message_queue.task_done()

    def check_message_queue(self):
        while not self.message_queue.empty():

            item = self.message_queue.get_nowait()

            if item.category == 'general':
                if item.payload == 'stop':
                    self.game.current_time = self.game.duration
                    self.mqtt_client.publish('/main-unit/game', "stopping game")
                    break
            elif item.category == 'mqtt':
                async_print("Received mqtt message: ", item.payload)
                self.game.handle_mqtt_message(item.payload)
            elif item.category == 'socket':
                async_print("Received socket message: ", item.payload)
                self.game.handle_socket_message(item.payload)

            else:
                self.mqtt_client.publish("/main-unit/log", f"received message {item}")
                async_print(item)

            self.message_queue.task_done()

    def run(self):
        async_print("Starting game thread")
        self.clear_msg_queue()
        while self.game.running:
            self.check_message_queue()
            self.game.step()
            self.mqtt_client.publish("/main-unit/game", str(self.game))
            time.sleep(0.01)

        self.mqtt_client.publish('/main-unit/game', "game finished")
        async_print("game ended")


class GameService:
    def __init__(self, game_repository: GameRepository, socket_manager, mqtt_client, msg_queue: GameMessageQueue):
        self.game_repository = game_repository
        self.game_process = None
        self.socket_manager = socket_manager
        self.mqtt_client = mqtt_client
        self.msg_queue = msg_queue

    def get_games(self) -> List[GameModel]:
        return self.game_repository.get_games()

    def get_leaderboard(self, game: str, difficulty: str) -> LeaderboardResponse:
        return self.game_repository.get_leaderboard(game, difficulty)

    def get_score(self):
        return self.game_repository.get_score()

    def setup_game(self, game_setup: GameConfigModel) -> GameStatusResponse:
        game = Game.from_config(game_setup)

        self.game_process = GameProcess(game, self.socket_manager, self.mqtt_client, self.msg_queue)
        self.game_process.start()
        # background_tasks.add_task(self.game_process.run)
        return GameStatusResponse(game=game_setup.game, teams=game_setup.teamNames, duration=game_setup.duration,
                                  difficulty=game_setup.difficulty, status="starting")
