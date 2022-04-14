import gym
from gym import spaces
from gym.utils import seeding

import numpy as np

class CoinGame(gym.Env):

    """
    ### Description
    The CoinGame environment is a simple game where the player has label an opponent as either a fair or a cheater.
    The player starts with 100 available flips.
    The player is rewarded with 15 flips for correctly labeling the opponent and -30 for incorrectly labeling the opponent.
    The player can flip one coin, flip five coins, label the opponent as fair, or label the opponent as cheater.
    The player loses when they do not have any flips remaining.

    ### Observation Space
    The observation is a 3-tuple containing the following:
    | Num | Observation                                                 | Min  | Max         | Unit   |
    |-----|-------------------------------------------------------------|------|-------------|--------|
    | 0   | Number of heads                                             | 0    | around 500  | amount |
    | 1   | Number of tails                                             | 0    | around 500  | amount |
    | 3   | Number of flips left                                        | 0    | around 500  | amount |
    
    ### Action Space
    There are 4 discrete actions:
    | Num | Action                                                      |
    |-----|-------------------------------------------------------------|
    | 0   | Flip one coin                                               |
    | 1   | Flip five coins                                             |
    | 2   | Label the current player as fair                            |
    | 3   | Label the current player as cheater                         |
    
       
    ### Reward:
    - Correctly labeling the opponent: 15 flips
    - Incorrectly labeling the opponent: -30 flips

    ### Episode Termination
    The episode terminates if either of the following happens:
    1. The position of the car is greater than or equal to 0.5 (the goal position on top of the right hill)
    2. The length of the episode is 200.
    """

    def __init__(self):
        #max_value = np.iinfo(np.int64).max
        max_value = 500
        self.observation_space =  spaces.Tuple(
            (spaces.Discrete(max_value), spaces.Discrete(max_value), spaces.Discrete(max_value))
        )
        self.action_space = spaces.Discrete(4)
        self.seed()

    def step(self, action: int):
        assert self.action_space.contains(action), f"{action!r} ({type(action)}) invalid"
        old_score = self.score

        new_score = self.score
        reward = new_score - old_score
        return self.get_data(), reward, self.done, {}

    def reset(self, return_info=False, seed=None):
        self.reset_game()
        if not return_info:
            return self.get_data()
        else:
            return self.get_data(), {}

    def close():
        raise NotImplementedError

    def reset_game(self):
        raise NotImplementedError

    def get_data(self) -> tuple: 
        raise NotImplementedError

    def flip_one_coin(self):
        raise NotImplementedError
    
    def flip_five_coins(self):
        raise NotImplementedError
    
    def toggle_show_flipping_animations(self):
        raise NotImplementedError
    
    def label_fair(self):
        raise NotImplementedError

    def label_cheater(self):
        raise NotImplementedError