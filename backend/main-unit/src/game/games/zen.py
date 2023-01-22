import random

from game.game import Game


class ZenGame(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_pole = 0
        self.number_of_poles = 0
        self.points = 0

        self.random_pole_on = False

    def select_random_pole(self):
        self.set_poles_off()
        self.current_pole = random.randint(0, self.number_of_poles - 1)
        self.random_pole_on = False

    def get_scores(self):
        return {
            "points": self.points
        }

    def prepare(self):
        self.number_of_poles = len(self.available_poles)
        self.select_random_pole()

    def handle_button_press(self, pole_id):
        if pole_id == self.available_poles[self.current_pole]:
            self.points += 1 # this needs to be changed later
            self.select_random_pole()

    def step(self):
        if not self.random_pole_on:
            self.set_pole_on(self.available_poles[self.current_pole])
            self.random_pole_on = True
