import random

from game.game import Game
from misc.queue import MessageQueue


class RedBlueGame(Game):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number_of_poles = 0
        self.scores = {tn: 0 for tn in self.team_names}

        self.team_pole = {tn: None for tn in self.team_names}

        self.team_colors = {}

        self.last_pole = None

    def prepare(self):
        self.number_of_poles = len(self.available_poles)

        for pole_id in self.available_poles:
            self.team_pole[pole_id] = None

        colors = [(255, 0, 0), (0, 0, 255)]

        for team in self.team_names:
            self.team_colors[team] = colors.pop()

    def on_pause(self):
        self.team_pole = {tn: None for tn in self.team_names}
        self.last_pole = None
        super().on_pause()

    def handle_button_press(self, pole_id):
        self.mqtt_log("Pole " + str(pole_id) + " has been pressed")
        for team_name in self.team_names:
            if self.team_pole[team_name] == pole_id:
                self.scores[team_name] += 1
                self.mqtt_log("Team " + team_name + " has scored")
                self.last_pole = self.team_pole[team_name]
                self.team_pole[team_name] = None
                self.choose_pole(team_name)

    def get_scores(self):
        for team, score in self.scores.items():
            print("Team " + team + " has " + str(score) + " points")
            yield [team, score]

    def choose_pole(self, team_name):
        available_poles = self.available_poles.copy()

        for team in self.team_names:
            if self.team_pole[team] is not None:
                available_poles.remove(self.team_pole[team])
            if self.last_pole is not None:
                available_poles.remove(self.last_pole)
                self.last_pole = None

        self.team_pole[team_name] = random.choice(available_poles)

        self.set_pole_on(self.team_pole[team_name], self.team_colors[team_name])
        self.mqtt_log("Pole " + str(self.team_pole[team_name]) + " is on for team " + team_name)

    def step(self):
        for team_name in self.team_names:
            if self.team_pole[team_name] is None:
                self.choose_pole(team_name)
