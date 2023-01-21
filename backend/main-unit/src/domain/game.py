import time

from misc.tools import async_print
from models.game_models import GameConfigModel


class Game:
    def __init__(self, duration: int, difficulty: str, game_name: str):
        self.duration = duration  # in seconds
        self.difficulty = difficulty
        self.game_name = game_name
        self.current_time = time.time()
        self.paused = False
        self.stopped = False
        self.elapsed_time = 0
        async_print("Game created")
        async_print(self)

    @classmethod
    def from_config(cls, game_config: GameConfigModel):
        return cls(game_config.duration, game_config.difficulty, game_config.game)

    @property
    def finished(self):
        return self.elapsed_time >= self.duration

    @property
    def running(self):
        return not self.finished

    def get_status(self):
        return {
            "game": self.game_name,
            "duration": self.duration,
            "current_time": self.current_time,
            "scores": self.get_scores(),
            "paused": self.paused,
            "finished": self.finished,
        }

    def get_scores(self):
        return {
            "team1": 0,
            "team2": 0
        }

    def step(self):
        if not self.paused:
            current_time = time.time()
            self.elapsed_time += current_time - self.current_time
        if self.stopped:
            self.elapsed_time = self.duration
        self.current_time = time.time()

    def handle_mqtt_message(self, message):
        async_print("mqtt message", message)
        async_print(self)
        if message == "pause":
            self.paused = True

    def handle_socket_message(self, message):
        async_print("socket message", message)

    def __str__(self):
        return f"Game({self.game_name}, total duration: {self.duration}, elapsed: {self.elapsed_time:.2f}, " \
               f"paused: {self.paused})"

    def __repr__(self):
        return self.__str__()
