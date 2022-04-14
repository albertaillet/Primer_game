# Albert Aillet, April 2022
# inspired by https://github.com/openai/gym/blob/master/gym/envs/toy_text/blackjack.py
# and https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
import gym
from gym import spaces, logger
from abc import abstractmethod


import numpy as np

class CoinGame(gym.Env):

    """
    ### Description
    The CoinGame environment is a simple game where the player has to label an opponent as either fair or a cheater.
    The player starts with 100 available flips.
    The player can use one flip for the opponent to flip their coin and the player can observe the outcome. 
    The opponent can either be fair and have a unbiased coin or be a cheater and have a coin that comes up heads too often.
    The player is rewarded with 15 flips for correctly labeling the opponent and -30 for incorrectly labeling the opponent.
    After labeling an opponent, they are replaced with another one with a different coin.
    The player can flip one coin, flip five coins, label the opponent as fair or label the opponent as cheater.
    The player loses when they have no flips remaining and labels the opponent incorrectly.

    ### Observation Space
    The observation is a 3-tuple containing the following:
    | Num | Observation                          | Min  | Max         | Unit   |
    |-----|--------------------------------------|------|-------------|--------|
    | 0   | Number of heads                      | 0    | around 100  | amount |
    | 1   | Number of tails                      | 0    | around 100  | amount |
    | 3   | Number of flips left                 | 0    | around 100  | amount |
    
    ### Action Space
    There are 4 discrete actions:
    | Num | Action                               |
    |-----|--------------------------------------|
    | 0   | Flip one coin                        |
    | 1   | Flip five coins                      |
    | 2   | Label the current player as fair     |
    | 3   | Label the current player as cheater  |
    
       
    ### Reward:
    - Correctly labeling the opponent: 15 flips
    - Incorrectly labeling the opponent: -30 flips

    ### Episode Termination
    - Player loses when they have no flips remaining and labels the opponent incorrectly.
    
    """

    def __init__(self):
        #max_value = np.iinfo(np.int64).max
        max_value = 100
        self.observation_space =  spaces.Tuple(
            (spaces.Discrete(max_value), spaces.Discrete(max_value), spaces.Discrete(max_value))
        )
        self.action_space = spaces.Discrete(4)
        self.seed()
        # the following properties are set by the subclass:
        self.score = 0
        self.flips_left = 0
        self.done = False


    def step(self, action: int) -> tuple:
        assert self.action_space.contains(action), f"{action!r} ({type(action)}) invalid"
        old_score = self.score
        old_flips = self.flips_left

        if action == 0:
            self.flip_one_coin()
        elif action == 1:
            self.flip_five_coins()
        elif action == 2:
            self.label_fair()
        elif action == 3:
            self.label_cheater()
        else: 
            raise ValueError(f"{action!r} ({type(action)}) invalid")
        
        data = self.observe()
        new_score = self.score
        new_flips = self.flips_left
        reward = new_flips - old_flips
        if self.done:
            logger.warn(
                "You are calling 'step()' even though this "
                "environment has already returned done = True. You "
                "should always call 'reset()' once you receive 'done = "
                "True' -- any further steps are undefined behavior."
            )
        return data, reward, self.done, {}

    def reset(self, return_info=False, seed=None):
        self.reset_game()
        if not return_info:
            return self.observe()
        else:
            return self.observe(), {}

    # The following methods have to be implmented by the class inheriting from this class.

    @abstractmethod
    def reset_game(self):
        raise NotImplementedError

    @abstractmethod
    def observe(self) -> tuple: 
        raise NotImplementedError

    @abstractmethod
    def flip_one_coin(self):
        raise NotImplementedError
    
    @abstractmethod
    def flip_five_coins(self):
        raise NotImplementedError
    
    @abstractmethod
    def toggle_show_flipping_animations(self):
        raise NotImplementedError
    
    @abstractmethod
    def label_fair(self):
        raise NotImplementedError

    @abstractmethod
    def label_cheater(self):
        raise NotImplementedError

    # The following methods are optional and can be implmented by the class inheriting from this class.
    
    @abstractmethod
    def render(self, mode='human'):
        raise NotImplementedError
    
    @abstractmethod
    def close(self, seed=None):
        raise NotImplementedError