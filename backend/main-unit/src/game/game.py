import enum
import re
import time

from misc.queue import MessageQueue
from misc.queue.mqtt import MQTTQueueItem
from misc.queue.socketio import SocketQueueItem
from misc.tools import async_print
from models.game_models import GameConfigModel, CurrentGameStatus


class OnButtonPressConfig(enum.Enum):
    LED_OFF = "led_off"
    LED_ON = "led_on"


class LedState(enum.Enum):
    ON = "on"
    OFF = "off"


class GameStatus(enum.Enum):
    NONE = "none"  # before the game is
    STOPPED = "stopped"  # when the game is stopped
    STARTING = "starting"  # before the game starts
    RUNNING = "running"  # during the game
    PAUSED = "paused"  # when the game is paused
    FINISHED = "finished"  # when the game is finished
    NOT_ENOUGH_POLES = "not_enough_poles"  # when there are not enough poles to play the game


class Game:
    on_button_press_config = OnButtonPressConfig.LED_OFF

    def __init__(self,
                 command_queue: MessageQueue,
                 game_config: GameConfigModel,
                 ):

        self.game_name = game_config.game
        self.game_config = game_config

        self.duration = game_config.duration
        self.difficulty = game_config.difficulty
        self.team_names = game_config.teamNames

        self.current_time = time.time()
        self.game_status = GameStatus.STARTING
        self.elapsed_time = 0

        self.available_poles = []

        self.__command_queue = command_queue

        async_print("Game created")
        async_print(self)

    @classmethod
    def from_config(cls, game_config: GameConfigModel, command_queue) -> "Game":
        if game_config.game == "zen":
            from game.games.zen import ZenGame
            async_print("Creating ZenGame")
            return ZenGame(command_queue, game_config)
        elif game_config.game == 'redblue':
            from game.games.redblue import RedBlueGame
            return RedBlueGame(command_queue, game_config)
        elif game_config.game == 'simonsays':
            from game.games.simonsays import SimonSaysGame
            return SimonSaysGame(command_queue, game_config)
        else:
            return cls(command_queue, game_config)

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
    def stopped(self):
        return self.game_status == GameStatus.STOPPED

    @property
    def running(self):
        return not self.paused and not self.finished

    def mqtt_log(self, message):
        self.send_mqtt_message("main-unit/log", message)

    def add_available_pole(self, pole_id):
        self.available_poles.append(pole_id)

    def send_mqtt_message(self, topic, message):
        self.__command_queue.put(MQTTQueueItem(topic, message))

    def get_status(self):
        return CurrentGameStatus(
            game=self.game_name,
            status=self.game_status.value,
            elapsed_time=self.elapsed_time,
            total_duration=self.duration,
            difficulty=self.difficulty,
            scores=self.get_scores()
        )

    def turn_all_poles_off(self):
        self.send_mqtt_message("command/all/light", "off")

    def on_pause(self):
        self.turn_all_poles_off()

    def on_stop(self):
        self.turn_all_poles_off()

    def thread_step(self):
        if len(self.available_poles) == 0:
            self.game_status = GameStatus.NOT_ENOUGH_POLES

        if not self.paused:
            current_time = time.time()
            self.elapsed_time += current_time - self.current_time

        if self.elapsed_time >= self.duration and not self.stopped:
            self.game_status = GameStatus.FINISHED
            self.elapsed_time = self.duration
            # async_print("Game finished, points:", self.get_scores())
            self.turn_all_poles_off()
            self.send_mqtt_message("notification/general", "Game finished")

        if self.game_status == GameStatus.STARTING:
            self.elapsed_time = 0
        self.current_time = time.time()

        if not self.paused:
            self.step()

    def send_socket_message(self, message):
        self.__command_queue.put(SocketQueueItem(message))

    def handle_mqtt_message(self, message: MQTTQueueItem):
        async_print("mqtt message", message)
        self.mqtt_log("handling mqtt message: " + str(message))

        if re.match(r"unit/[A-Za-z0-9]+/action", message.topic):
            pole_id = int(message.topic.split("/")[1])
            self.handle_button_press(pole_id)

    def handle_socket_message(self, message):
        async_print("socket message", message)

        if message == 'pause':
            self.game_status = GameStatus.PAUSED
            self.on_pause()
        elif message == 'resume':
            self.game_status = GameStatus.RUNNING
        elif message == 'start':
            self.game_status = GameStatus.RUNNING
        elif message == 'stop':
            self.game_status = GameStatus.STOPPED
            self.on_stop()

    def set_pole_on(self, pole_id, color: tuple = (255, 255, 255)):
        self.send_mqtt_message(f"command/{pole_id}/light", f"on {color[0]} {color[1]} {color[2]}")

    def set_pole_off(self, pole_id):
        self.send_mqtt_message(f"command/{pole_id}/light", "off")

    def set_poles_off(self):
        self.send_mqtt_message(f'command/all/light', 'off')

    def set_poles_on(self, color: tuple = (255, 255, 255)):
        self.send_mqtt_message(f'command/all/light', f'on {color[0]} {color[1]} {color[2]}')

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
