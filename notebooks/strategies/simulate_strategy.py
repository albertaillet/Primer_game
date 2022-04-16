import os, sys
import numpy as np
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from game_simulation import CoinGameSimulation

def simulate_strategy(strategy, n_simulations=500):
    # Simulate the game with the given strategy
    # strategy is a function that takes n_heads, n_tails and flips_left and returns an action in ("fair", "cheater", "one_flip", "five_flips")
    g = CoinGameSimulation()
    scores = []
    n_labels_list = []
    n_flips_list = []
    n_flips_per_label_list = []
    rewards = []
    for _ in range(n_simulations):
        n_heads, n_tails, flips_left = g.reset()
        n_labels = 0
        n_flips = 0
        n_flips_per_label = 0
        done = g.done
        while not done:
            action = strategy(n_heads, n_tails, flips_left)
            (n_heads, n_tails, flips_left), reward, done, _ = g.step(action)
            rewards.append(reward)

            if action == 2:
                n_labels += 1
                n_flips_per_label_list.append(n_flips_per_label)
                n_flips_per_label = 0
            elif action == 3:
                n_labels += 1
                n_flips_per_label_list.append(n_flips_per_label)
                n_flips_per_label = 0
            elif action == 0:
                n_flips_per_label += 1
                n_flips += 1
            elif action == 1:
                n_flips_per_label += 5
                n_flips += 5
            else:
                raise ValueError("Unknown action: {}".format(action))
        scores.append(g.score)
        n_labels_list.append(n_labels)
        n_flips_list.append(n_flips)
    
    for name, l in zip(["score", "n_labels", "n_flips_per_game", "n_flips_per_label", "reward"],[scores, n_labels_list, n_flips_list, n_flips_per_label_list, rewards]):
        print(name, np.mean(l), "±", np.std(l))