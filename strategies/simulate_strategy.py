from cProfile import label
import os, sys
import numpy as np
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from game_simulation import CoinGameSimulation

def simulate_strategy(strategy, n_simulations=500):
    # Simulate the game with the given strategy
    # strategy is a function that takes n_heads, n_tails and flips_left and returns an action in ("fair", "cheater", "one_flip", "five_flips")
    g = CoinGameSimulation()
    scores = []
    true_labels = []
    prediced_labels = []
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
            
            if action == 2:
                n_labels += 1
                n_flips_per_label_list.append(n_flips_per_label)
                n_flips_per_label = 0
                prediced_labels.append(0)
                true_labels.append(g.opponent.ground_truth_label)
            elif action == 3:
                n_labels += 1
                n_flips_per_label_list.append(n_flips_per_label)
                n_flips_per_label = 0
                prediced_labels.append(1)
                true_labels.append(g.opponent.ground_truth_label)
            elif action == 0:
                n_flips_per_label += 1
                n_flips += 1
            elif action == 1:
                n_flips_per_label += 5
                n_flips += 5
            else:
                raise ValueError("Unknown action: {}".format(action))

            (n_heads, n_tails, flips_left), reward, done, _ = g.step(action)
            rewards.append(reward)

        scores.append(g.score)
        n_labels_list.append(n_labels)
        n_flips_list.append(n_flips)
    
    for name, l in zip(["Score", "Labels per game", "Flips per game", "Flips per label", "Reward"],[scores, n_labels_list, n_flips_list, n_flips_per_label_list, rewards]):
        print(f"{name:15} mean: {np.mean(l):5.2f}, std: {np.std(l):5.2f}, median {int(np.median(l)):3}, min: {np.min(l):3}, max: {np.max(l):3}")


    true_labels = np.array(true_labels)
    prediced_labels = np.array(prediced_labels)

    accuracy = np.mean(prediced_labels == true_labels)

    TP = ((true_labels == prediced_labels) & (true_labels == 0)).sum()
    TN = ((true_labels == prediced_labels) & (true_labels == 1)).sum()

    FP = ((true_labels != prediced_labels) & (true_labels == 0)).sum()
    FN = ((true_labels != prediced_labels) & (true_labels == 1)).sum()

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall)
    print(f"Accuracy: {accuracy:5.3f}, Precision: {precision:5.3f}, Recall: {recall:5.3f}, F1-score: {f1:5.3f}")
