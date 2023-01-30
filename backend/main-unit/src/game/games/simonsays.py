import random
import time

from game.game import Game
from misc.tools import async_print

COLOR_CYCLE = [(0, 0, 255), (75, 0, 130), (0, 139, 139), (255, 105, 180)]


class SimonSays(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
