# Albert Aillet, April 2022
# Implements the simulated logic of the game.
import random
from game import CoinGame

class CoinGameSimulation(CoinGame):

    def __init__(self):
        super().__init__()
        self.correct_label_bonus = 15
        self.incorrect_label_penalty = -30
        self.start_flips = 100
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.flips_left = self.start_flips
        self.new_opponent()
        self.done = False
    
    def new_opponent(self):
        self.opponent = Opponent()
        self.heads = 0
        self.tails = 0

    def observe(self) -> tuple: 
        return self.heads, self.tails, self.flips_left 
    
    def flip_one_coin(self):
        if self.flips_left > 0:
            if self.opponent.flip():
                self.heads += 1
            else:
                self.tails += 1
            self.flips_left -= 1
    
    def flip_five_coins(self):
        for _ in range(5):
            self.flip_one_coin()
    
    def label_fair(self):
        self._label(0)

    def label_cheater(self):
        self._label(1)

    def _label(self, label: str):
        if label == self.opponent.ground_truth_label:
            self.score += 1
            self.flips_left += self.correct_label_bonus
        else:
            self.flips_left += self.incorrect_label_penalty
        self.new_opponent()
        if self.flips_left < 0:
            self.done = True


class Opponent():

    def __init__(self) -> None:
        # 0: fair, 1: cheater
        unif = random.random()
        if unif > 0.5:
            self.p = 0.75
            self.ground_truth_label = 1
        else:
            self.p = 0.5
            self.ground_truth_label = 0
    
    def flip(self) -> bool:
        # True: heads, False: tails
        return random.random() < self.p