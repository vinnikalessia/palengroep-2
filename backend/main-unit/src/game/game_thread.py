import threading
import time
from queue import Queue

from fastapi_mqtt import FastMQTT

from game.game import Game, GameStatus
from misc.queue import MessageQueue
from misc.queue.item import QueueItem
from misc.queue.mqtt import MQTTQueueItem
from misc.queue.pole_action import PoleActionQueueItem
from misc.tools import async_print
from models.game_models import GameConfigModel, GameScore, CurrentGameStatus
from repositories.game_repository import GameRepository


class GameThread(threading.Thread):

    def __init__(self,
                 game_config: GameConfigModel,
                 mqtt_client,
                 client_queue: MessageQueue):

        self.client_queue = client_queue
        self.game_repository = GameRepository()
        self.server_queue = Queue()

        self.mqtt_client: FastMQTT = mqtt_client

        self.stopped = False

        self.game_config = game_config
        self.game = Game.from_config(game_config=self.game_config, command_queue=self.server_queue)

        super().__init__(name="game thread")

    def _log_mqtt(self, message):
        self.mqtt_client.publish('main-unit/log', message)

    def stop(self):
        self.client_queue.put(QueueItem("general", "stop"))

    def clear_client_queue(self):
        while not self.client_queue.empty():
            self.client_queue.get_nowait()
            self.client_queue.task_done()

    def add_alive_esp32(self, esp32_id):
        self.game.add_available_pole(esp32_id)

    def handle_general_message(self, payload):
        if payload == 'stop':
            self.game.current_time = self.game.duration
            self.stopped = True
            self._log_mqtt("stopping game")
            self.game.on_stop()
            self.game.game_status = GameStatus.STOPPED
        elif payload == 'pause':
            self.game.game_status = GameStatus.PAUSED
            self.game.on_pause()
            self._log_mqtt("pausing game")
        elif payload == 'resume':
            self.game.game_status = GameStatus.RUNNING
            self._log_mqtt("resuming game")
        elif payload == 'start':
            self.game.game_status = GameStatus.RUNNING
            self._log_mqtt("starting game")

    def check_client_queue(self):
        while not self.client_queue.empty():

            item = self.client_queue.get_nowait()
            self._log_mqtt("received message " + str(item))

            if item.category == 'general':
                async_print("Received general message: ", item.payload)
                self.handle_general_message(item.payload)

            elif item.category == 'mqtt':
                async_print("Received mqtt message: ", item.payload)

                assert isinstance(item, MQTTQueueItem)
                if item.topic.endswith('/alive'):
                    self.add_alive_esp32(item.payload)
                else:
                    self.game.handle_mqtt_message(item)

            elif item.category == 'pole':
                async_print("Received pole message: ", item.payload)
                if isinstance(item, PoleActionQueueItem):
                    self.game.handle_button_press(item.pole_id)

            elif item.category == 'socket':
                async_print("Received socket message: ", item.payload)
                self.game.handle_socket_message(item.payload)

            else:
                self._log_mqtt(f"received message {item}")
                async_print(item)

            self.client_queue.task_done()

    def check_server_queue(self):
        while not self.server_queue.empty():
            item = self.server_queue.get_nowait()

            if item.category == 'mqtt':
                assert isinstance(item, MQTTQueueItem)
                print(item)
                self.mqtt_client.publish(item.topic, item.payload)

            else:
                self._log_mqtt(f"received message {item}")
                async_print(item)
            self.server_queue.task_done()

    def wait_for_esp32s(self):
        self._log_mqtt("waiting for esp32s to connect")
        time.sleep(1)
        self.check_client_queue()

    def prepare_game(self):
        self._log_mqtt("preparing game")
        self.mqtt_client.publish('notification/general', 'GAME_START_NOTIFICATION')
        self.wait_for_esp32s()

        self._log_mqtt("configuring poles")
        self.mqtt_client.publish('configure/all/on_press', self.game.on_button_press_config.value)

        self.game.prepare()

    def get_score(self) -> GameScore:
        scores = {}
        for team, score in self.game.get_scores():
            scores[team] = score
        return GameScore(game=self.game.game_name, difficulty=self.game.difficulty, scores=scores)

    def save_game(self):
        async_print("saving game")

        for team, score in self.game.get_scores():
            async_print(f"team {team} scored {score} points")
            self.game_repository.save_score(self.game_config.game, self.game_config.difficulty, team, score)

        async_print("game saved")

    def turn_off_lights(self):
        self.mqtt_client.publish('command/all/light', 'off')

    def get_game_status(self) -> CurrentGameStatus:
        if self.game is not None:
            return self.game.get_status()
        else:
            return CurrentGameStatus(
                game="",
                difficulty="",
                status=GameStatus.NONE.value,
                elapsed_time=0,
                total_duration=0,
                scores={}
            )

    def run(self):

        self.clear_client_queue()

        self.prepare_game()
        self._log_mqtt('ready to start game')

        while self.game.starting:
            self.check_client_queue()
            time.sleep(0.01)

        while not self.stopped and (self.game.running or self.game.paused) \
                and self.game.game_status != GameStatus.NOT_ENOUGH_POLES:
            self.check_client_queue()
            self.game.thread_step()
            self.check_server_queue()
            time.sleep(0.01)

        if not self.stopped and self.game.game_status != GameStatus.NOT_ENOUGH_POLES:
            self.save_game()
        else:
            self._log_mqtt("game stopped, not saving")
        self._log_mqtt("game finished")

        self.turn_off_lights()

        async_print("game ended")
