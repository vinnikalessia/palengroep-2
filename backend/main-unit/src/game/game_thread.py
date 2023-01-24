import threading
import time
from queue import Queue

from fastapi_mqtt import FastMQTT

from game.game import Game, GameStatus
from misc.queue import MessageQueue
from misc.queue.item import QueueItem
from misc.queue.mqtt import MQTTQueueItem
from misc.queue.socketio import SocketQueueItem
from misc.tools import async_print
from models.game_models import GameConfigModel


class GameThread(threading.Thread):
    def __init__(self,
                 game_config: GameConfigModel,
                 socket_manager, mqtt_client,
                 client_queue: MessageQueue):
        self.client_queue = client_queue
        self.server_queue = Queue()

        self.socket_manager = socket_manager
        self.mqtt_client: FastMQTT = mqtt_client

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
            self.game.stopped = True
            self._log_mqtt("stopping game")
        elif payload == 'pause':
            self.game.game_status = GameStatus.PAUSED
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
            elif item.category == 'socket':
                assert isinstance(item, SocketQueueItem)
                self.socket_manager.emit(item.payload)
            else:
                self._log_mqtt(f"received message {item}")
                async_print(item)
            self.server_queue.task_done()

    def wait_for_esp32s(self):
        self._log_mqtt("waiting for esp32s to connect")
        time.sleep(2)
        self.check_client_queue()

    def prepare_game(self):
        self._log_mqtt("preparing game")
        self.mqtt_client.publish('notification/general', 'GAME_START_NOTIFICATION')
        self.wait_for_esp32s()

        self._log_mqtt("configuring poles")
        self.mqtt_client.publish('configure/all/on_press', self.game.on_button_press_config.value)

        self.game.prepare()

    def run(self):
        self.clear_client_queue()

        self.prepare_game()
        self._log_mqtt('ready to start game')

        self.socket_manager.emit('game_ready', "yess")

        while self.game.starting:
            self.check_client_queue()
            time.sleep(0.01)

        while self.game.running:
            self.check_client_queue()
            self.game.thread_step()
            self.check_server_queue()
            time.sleep(0.01)

        self._log_mqtt("game finished")
        async_print("game ended")
        del self.game
