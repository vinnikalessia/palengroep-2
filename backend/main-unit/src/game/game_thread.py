import threading
import time

from fastapi_mqtt import FastMQTT

from domain.game import Game
from misc.queue import GameMessageQueue
from misc.queue.items.item import QueueItem
from misc.tools import async_print


class GameThread(threading.Thread):
    def __init__(self, game: Game, socket_manager, mqtt_client,
                 message_queue: GameMessageQueue):
        self.socket_manager = socket_manager
        self.mqtt_client: FastMQTT = mqtt_client
        self.game = game
        self.message_queue = message_queue
        self.alive_esp32 = set()
        super().__init__(name="game thread")

    def _log_mqtt(self, message):
        self.mqtt_client.publish('main-unit/log', message)

    def stop(self):
        self.message_queue.put(QueueItem("general", "stop"))

    def clear_msg_queue(self):
        while not self.message_queue.empty():
            self.message_queue.get_nowait()
            self.message_queue.task_done()

    def add_alive_esp32(self, esp32_id):
        self.alive_esp32.add(esp32_id)

    def handle_general_message(self, payload):
        if payload == 'stop':
            self.game.current_time = self.game.duration
            self.game.stopped = True
            self._log_mqtt("stopping game")
        elif payload == 'pause':
            self.game.paused = True
            self._log_mqtt("pausing game")

    def check_message_queue(self):
        while not self.message_queue.empty():

            item = self.message_queue.get_nowait()

            if item.category == 'general':
                async_print("Received general message: ", item.payload)
                self.handle_general_message(item.payload)

            elif item.category == 'mqtt':
                async_print("Received mqtt message: ", item.payload)
                self.game.handle_mqtt_message(item.payload)

            elif item.category == 'socket':
                async_print("Received socket message: ", item.payload)
                self.game.handle_socket_message(item.payload)

            else:
                self._log_mqtt(f"received message {item}")
                async_print(item)

            self.message_queue.task_done()

    def run(self):
        async_print("Starting game thread")
        self.clear_msg_queue()
        while self.game.running:
            self.check_message_queue()
            self.game.step()
            self._log_mqtt(str(self.game))
            time.sleep(0.01)

        self._log_mqtt("game finished")
        async_print("game ended")
