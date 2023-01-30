import random
import time

from game.game import Game
from misc.tools import async_print

COLOR_CYCLE = [(0, 0, 255), (75, 0, 130), (0, 139, 139), (255, 105, 180)]


class SimonSaysGame(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_index = 0
        self.current_turn = "simon"  # "simon" or "player"
        self.continue_after = 0
        self.sequence = []

        self.scheduled_events = []

        self.game_over = False  # if the game is over, light up all the poles as red

        self.off_after_continue = False

        self.timeout_seconds = 10 if self.difficulty.lower() == "traag" else 5

    def prepare(self):
        self.sequence = [random.choice(self.available_poles)]
        self.reset_timer()

    def handle_button_press(self, pole_id):
        self.turn_all_poles_off()

        pole_color = COLOR_CYCLE[self.current_index % len(COLOR_CYCLE)]
        self.set_pole_on(pole_id, pole_color)
        self.continue_after = time.time() + 0.5
        self.scheduled_events.append("light off")
        self.reset_timer()

        if self.sequence[self.current_index] == pole_id:
            self.current_index += 1

            if self.current_index == len(self.sequence):
                self.scheduled_events.append("good sequence")

        else:
            self.scheduled_events.append("bad sequence")

    def on_pause(self):
        super().on_pause()
        self.elapsed_time = 0

    def reset_timer(self):
        self.elapsed_time = 0
        self.duration = self.timeout_seconds

    def done_good_sequence(self):
        # if the player has done the sequence correctly,
        # light up all poles for 2 seconds in green,
        # then add a new pole to the sequence and let simon start again

        self.current_turn = "simon"
        self.current_index = 0
        self.sequence.append(random.choice(self.available_poles))
        self.set_poles_on((0, 255, 0))
        self.continue_after = time.time() + 2

    def done_bad_sequence(self):
        # if the player has done the sequence incorrectly, light up all poles for 2 seconds in red
        self.set_poles_on((255, 0, 0))
        self.continue_after = time.time() + 2
        self.game_over = True

    def get_scores(self):
        score = len(self.sequence) - 1

        if self.difficulty.lower() != "traag":
            score *= 1.25
            score = round(score)

        yield [self.team_names[0], score]

    def step(self):
        if time.time() < self.continue_after:
            if "light off" in self.scheduled_events:
                self.reset_timer() # dirtyyyy
            return

        if len(self.scheduled_events) > 0:
            event = self.scheduled_events.pop(0)

            if event == "good sequence":
                self.done_good_sequence()
            elif event == "bad sequence":
                self.done_bad_sequence()
            elif event == "light off":
                self.turn_all_poles_off()
                self.continue_after = time.time() + 0.5
            else:
                async_print("Unknown scheduled event: " + event)
            return

        if self.game_over:
            self.duration = 0  # end the game, it is dirty but it works
            return

        if self.current_turn == "simon":
            self.turn_all_poles_off()
            self.reset_timer()
            if self.current_index == len(self.sequence):
                self.current_turn = "player"
                self.current_index = 0
            else:
                color_index = self.current_index % len(COLOR_CYCLE)
                self.set_pole_on(self.sequence[self.current_index], COLOR_CYCLE[color_index])
                self.current_index += 1

                self.continue_after = time.time() + 1

        elif self.current_turn == "player":
            if self.elapsed_time > self.timeout_seconds:
                self.done_bad_sequence()
