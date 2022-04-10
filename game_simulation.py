import time
import numpy as np


class Player():

    def __init__(self) -> None:
        player = Player()




class CoinGameSimulation():

    def __init__(self):
        self.reset_data()
        
    def reset_data(self):
        self.heads = None
        self.tails = None
        self.score = None
        self.flips_left = None
    
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
        self.heads = None
        self.tails = None
        self.score = None
        self.flips_left = None

        return {k:v for k, v in zip(["heads", "tails", "score", "flips_left"], [self.heads, self.tails, self.score, self.flips_left])}
    
    
    def flip_one_coin(self):
        pass
    
    def flip_five_coins(self):
        pass
    
    def toggle_show_flipping_animations(self):
        pass
    
    def label_fair(self):
        pass

    def label_cheater(self):
        pass

    def reset_game(self):
        self.__init__