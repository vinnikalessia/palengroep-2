import random
import time

from game.game import Game
from misc.tools import async_print


class ZenGame(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_pole = 0
        self.number_of_poles = 0
        self.points = 0

        self.timeout_seconds = 5 if self.difficulty.lower() == "traag" else 2.5

        self.blink_counter = 0
        self.blink_status = None
        self.last_blink = time.time()

        self.random_pole_on = False
        self.time_pole_on = time.time()
        self.time_pole_off = time.time() + self.timeout_seconds

    def select_random_pole(self):
        self.set_poles_off()
        self.current_pole = random.randint(0, self.number_of_poles - 1)
        self.random_pole_on = False

    def get_scores(self):
        yield [self.team_names[0], self.points]

    def prepare(self):
        self.number_of_poles = len(self.available_poles)
        self.select_random_pole()
        self.blink_counter = 5

    def calculate_points(self, reaction_time):
        score = (self.timeout_seconds - reaction_time) * 1.5
        if self.difficulty.lower() == "traag":
            return round(score // 2)
        else:
            return round(score)

    def handle_button_press(self, pole_id):
        if pole_id == self.available_poles[self.current_pole]:
            reaction_time = time.time() - self.time_pole_on
            self.points += self.calculate_points(reaction_time)
            self.random_pole_on = False
            self.blink_counter = 5

            async_print("button pressed !!")

    def set_pole_on(self, pole_id, color: tuple = (0, 255, 0)):
        super().set_pole_on(pole_id, color)

    def step(self):
        if self.blink_counter > 0:
            if time.time() - self.last_blink > 0.5:
                self.blink_counter -= 1
                self.last_blink = time.time()

                if self.blink_counter % 2 == 1 and self.blink_status != "on":
                    self.set_poles_on()
                    self.blink_status = "on"
                elif self.blink_counter % 2 == 0 and self.blink_status != "off":
                    self.set_poles_off()
                    self.blink_status = "off"

        elif not self.random_pole_on:

            self.select_random_pole()
            self.set_pole_on(self.available_poles[self.current_pole])
            self.random_pole_on = True
            self.mqtt_log("Pole " + str(self.current_pole) + " is on")
            self.time_pole_on = time.time()
            self.time_pole_off = time.time() + self.timeout_seconds
        else:
            if time.time() > self.time_pole_off:
                self.random_pole_on = False
                self.select_random_pole()
                self.set_poles_off()
                self.blink_counter = 5
