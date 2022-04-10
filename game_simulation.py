import random

class CoinGameSimulation():

    def __init__(self):     
        self.correct_label_bonus = 15
        self.incorrect_label_penalty = -30
        self.start_flips = 100

        self.score = 0
        self.flips_left = self.start_flips

        self.new_blob()

        self.game_over = False
    
    def new_blob(self):
        self.player = Player()
        self.heads = 0
        self.tails = 0
    
    def get_score(self) -> int:
        if self.score is None:
            self.get_data()
        return self.score

    def get_flips_left(self) -> int:
        if self.flips_left is None:
            self.get_data()
        return self.flips_left
    
    def get_heads(self) -> int:
        if self.heads is None:
            self.get_data()
        return self.heads

    def get_tails(self) -> int:
        if self.tails is None:
            self.get_data()
        return self.tails

    def get_data(self) -> dict: 
        return {k:v for k, v in zip(["heads", "tails", "score", "flips_left"], [self.heads, self.tails, self.score, self.flips_left])}
    
    
    def flip_one_coin(self):
        if self.flips_left > 0:
            if self.player.flip():
                self.heads += 1
            else:
                self.tails += 1
            self.flips_left -= 1
    
    def flip_five_coins(self):
        for _ in range(5):
            self.flip_one_coin()
    
    def label_fair(self):
        self._label("fair")

    def label_cheater(self):
        self._label("cheater")

    def _label(self, label: str):
        if label == self.player.ground_truth_label:
            self.score += 1
            self.flips_left += self.correct_label_bonus
        else:
            self.flips_left += self.incorrect_label_penalty
        self.new_blob()
        if self.flips_left <= 0:
            self.game_over = True

    def reset_game(self):
        self.__init__()


class Player():

    def __init__(self) -> None:
        if random.random() < 0.5:
            self.p = random.random() * 0.5 + 0.5
            self.ground_truth_label = "cheater"
        else:
            self.p = 0.5
            self.ground_truth_label = "fair"
    
    def flip(self) -> bool:
        # True: heads, False: tails
        return random.random() < self.p