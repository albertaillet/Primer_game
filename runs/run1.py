import time
from ..game import CoinGame

g = CoinGame()

iterations = 0
with open('log1.txt', 'w') as f:
    f.write('Score, Flips left, Heads, Tails, Difference\n')


while g.get_flips_left() is None or g.get_flips_left() > 0:
    iterations += 1
    counts = g.get_flips()
    score = g.get_score()
    flips_left = g.get_flips_left()
    n_heads = counts['Heads']
    n_tails = counts['Tails']
    n_throws = n_heads + n_tails
    diff = (n_heads-n_tails)

    with open('log1.txt', 'a') as f:
        f.write(f'{score:3},{flips_left:3},{n_heads:2},{n_tails:2},{diff:2}\n')
    print(f'{score:3},{flips_left:3},{n_heads:2},{n_tails:2},{diff:2}')

    if diff > 4:
        g.label_cheater()
        time.sleep(2)
    elif diff < -2 or (n_throws > 10 and diff < 2):
        g.label_fair()
        time.sleep(2)
    g.flip_one_coin()

g.get_page_screenshot().save("run1_final_score.png")