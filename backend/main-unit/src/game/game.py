import enum
import re
import time

from misc.queue import MessageQueue
from misc.queue.mqtt import MQTTQueueItem
from misc.queue.socketio import SocketQueueItem
from misc.tools import async_print
from models.game_models import GameConfigModel


class OnButtonPressConfig(enum.Enum):
    LED_OFF = "led_off"
    LED_ON = "led_on"


class LedState(enum.Enum):
    ON = "on"
    OFF = "off"


class GameStatus(enum.Enum):
    STARTING = "starting"  # before the game starts
    RUNNING = "running"  # during the game
    PAUSED = "paused"  # when the game is paused
    FINISHED = "finished"  # when the game is finished


class Game:
    on_button_press_config = OnButtonPressConfig.LED_OFF

    def __init__(self,
                 command_queue: MessageQueue,
                 duration: int = 60,
                 difficulty: str = "traag",
                 game_name: str = "zen"):

        self.game_name = game_name

        self.duration = duration  # in seconds
        self.difficulty = difficulty

        self.current_time = time.time()
        self.game_status = GameStatus.STARTING
        self.elapsed_time = 0

        self.available_poles = []

        self.__command_queue = command_queue

        async_print("Game created")
        async_print(self)

    @classmethod
    def from_config(cls, game_config: GameConfigModel, command_queue):
        if game_config.game == "zen":
            from game.games.zen import ZenGame
            return ZenGame(command_queue, game_config.duration, game_config.difficulty, game_config.game)
        elif game_config.game == 'red/blue':
            # from game.games.red_blue import RedBlueGame
            # return RedBlueGame(game_config.duration, game_config.difficulty, game_config.game)
            pass
        else:
            return cls(command_queue, game_config.duration, game_config.difficulty, game_config.game)

    @property
    def paused(self):
        return self.game_status == GameStatus.PAUSED

    @property
    def starting(self):
        return self.game_status == GameStatus.STARTING

    @property
    def finished(self):
        return self.game_status == GameStatus.FINISHED

    @property
    def running(self):
        return not self.paused and not self.finished

    def add_available_pole(self, pole_id):
        self.available_poles.append(pole_id)

    def get_status(self):
        return {
            "game": self.game_name,
            "duration": self.duration,
            "current_time": self.current_time,
            "scores": self.get_scores(),
            "paused": self.paused,
            "finished": self.finished,
        }

    def thread_step(self):
        if not self.game_status == GameStatus.PAUSED:
            current_time = time.time()
            self.elapsed_time += current_time - self.current_time

            if self.elapsed_time >= self.duration:
                self.game_status = GameStatus.FINISHED
                self.elapsed_time = self.duration
                async_print("Game finished")
                self.send_mqtt_message("command/all/light", "off")

        if self.game_status == GameStatus.STARTING:
            self.elapsed_time = self.duration
        self.current_time = time.time()

        self.step()

    def send_mqtt_message(self, topic, message):
        self.__command_queue.put(MQTTQueueItem(topic, message))

    def send_socket_message(self, message):
        self.__command_queue.put(SocketQueueItem(message))

    def handle_mqtt_message(self, message: MQTTQueueItem):
        async_print("mqtt message", message)

        if re.match(r"unit/[A-Za-z0-9]+/action", message.topic):
            pole_id = int(message.topic.split("/")[1])
            self.handle_button_press(pole_id)

    def handle_socket_message(self, message):
        async_print("socket message", message)

        if message == 'pause':
            self.game_status = GameStatus.PAUSED
        elif message == 'resume':
            self.game_status = GameStatus.RUNNING
        elif message == 'start':
            self.game_status = GameStatus.RUNNING
        elif message == 'stop':
            self.game_status = GameStatus.FINISHED

    def set_pole_on(self, pole_id, color: tuple = (255, 255, 255)):
        self.send_mqtt_message(f"command/{pole_id}/light", f"on {color[0]} {color[1]} {color[2]}")

    def set_poles_off(self):
        self.send_mqtt_message(f'command/all/light', 'off')

    def prepare(self):
        pass

    def handle_button_press(self, pole_id):
        raise NotImplementedError("handle_button_press() not implemented")

    def get_scores(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError("step() not implemented")

    def __str__(self):
        return f"Game({self.game_name}, total duration: {self.duration}, elapsed: {self.elapsed_time:.2f}, " \
               f"paused: {self.paused})"

    def __repr__(self):
        return self.__str__()
