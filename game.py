"""
April 2022
inspired by https://github.com/openai/gym/blob/master/gym/envs/toy_text/blackjack.py
and https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
"""
import gym
from gym import spaces, logger
from abc import abstractmethod


class CoinGame(gym.Env):
    """
    ### Description
    The CoinGame environment is a simple game where the player has to label an opponent as either fair or a cheater.
    The player starts with 100 available flips.
    The player can use one flip for the opponent to flip their coin and the player can observe the outcome.
    The opponent can be fair with a probability of 50% and have a unbiased coin that flips heads 50% of the time.
    The opponent can be a cheater with a probability of 50% and have a biased coin that flips heads 75% of the time.
    The player is rewarded with 15 extra flips for correctly labeling the opponent and -30 for incorrectly labeling
    the opponent. After labeling an opponent, they are replaced with another one with a different coin.
    The player can flip one coin, flip five coins, label the opponent as fair or label the opponent as cheater.
    The player loses when they have no flips remaining and labels the opponent incorrectly.

    ### Observation Space
    The observation is a 3-tuple containing the following:
    | Num | Observation                          | Min  | Max             | Unit   |
    |-----|--------------------------------------|------|-----------------|--------|
    | 0   | Number of heads                      | 0    | Inf (set to 99) | amount |
    | 1   | Number of tails                      | 0    | Inf (set to 99) | amount |
    | 3   | Number of flips left                 | 0    | Inf             | amount |
    
    ### Action Space
    There are 4 discrete actions:
    | Num | Action                               |
    |-----|--------------------------------------|
    | 0   | Flip one coin                        |
    | 1   | Flip five coins                      |
    | 2   | Label the current player as fair     |
    | 3   | Label the current player as cheater  |
       
    ### Reward:
    - Flipping one coin: -1 flip
    - Flipping five coins: -5 flips
    - Correctly labeling the opponent: 15 flips
    - Incorrectly labeling the opponent: -30 flips

    ### Episode Termination
    - Player loses when they have no flips remaining and labels the opponent incorrectly.
    """

    def __init__(self):     
        self.observation_space = spaces.Tuple(
            (spaces.Discrete(99), spaces.Discrete(99), spaces.Discrete(1000))
        )
        self.action_space = spaces.Discrete(4)
        self.seed()
        self.correct_label_bonus = 15
        self.incorrect_label_penalty = -30
        self.start_flips = 100
        self.heads = 0
        self.tails = 0
        self.score = 0
        self.flips_left = self.start_flips
        self.done = False

    def step(self, action: int) -> tuple:
        assert self.action_space.contains(action), f"{action!r} ({type(action)}) invalid"
        if self.done:
            logger.warn(
                "You are calling 'step()' even though this "
                "environment has already returned done = True. You "
                "should always call 'reset()' once you receive 'done = "
                "True' -- any further steps are undefined behavior."
            )
        
        old_flips_left = self.flips_left

        if action == 0:
            self.flip_one_coin()
        elif action == 1:
            self.flip_five_coins()
        elif action == 2:
            self.label_fair()
        elif action == 3:
            self.label_cheater()
        
        data = self.observe()
        new_score, new_flips_left = self.score, self.flips_left
        
        # reward is the number of gained or lost flips from the previous state
        reward = new_flips_left - old_flips_left
        return data, reward, self.done, {"score": new_score}

    def reset(self, return_info=False, seed=None):
        self.reset_game()
        if not return_info:
            return self.observe()
        else:
            return self.observe(), {}

    def render(self, mode='human'):
        if mode == 'human':
            return ("Heads: {} \n"
                    "Tails: {} \n"
                    "Score: {} \t Flips left: {} \n"
                    "Done: {} \n"
                    ).format(self.heads, self.tails, self.score, self.flips_left, self.done)

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
    def label_fair(self):
        raise NotImplementedError

    @abstractmethod
    def label_cheater(self):
        raise NotImplementedError
