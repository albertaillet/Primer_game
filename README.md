## Primer game:

This is a repository with environments for simulating and interacting with the game from [Coin Flip Cheaters: A game from Primer](https://www.youtube.com/watch?v=QC91Bf8hQVo).

[`game.py`](game.py) includes the class `CoinGame` that inherits from the openai [`gym.Env`](https://github.com/openai/gym/blob/master/gym/core.py) base class to set up the environment.

[`game_simulation.py`](game_simulation.py) includes the class `CoinGameSimulation` implements a simulation of the game to test out the your strategies or models.

[`game_browser.py`](game_browser.py) includes the class `CoinGameBrowser` iteracts with the online game at [primerlearning.org](https://primerlearning.org/).

## Strategies:

My strategies can be found in the `strategies` directory.
The most succestful one was the simple bayesian strategy as we are given the probabilities of the simulation.

## How to use:

To get exactly the same dependencies as I used, create the conda environment using:

```bash
conda env create -f environment.yml
```

To use the simulation here is an example, the simulation uses the [gym](https://github.com/openai/gym/) API:

```python
from game_simulation import CoinGameSimulation

def strategy(n_heads, n_tails, flips_left):
    # define your strategy here
    # see game.py for more details
    return 

g = CoinGameSimulation()

(n_heads, n_tails, flips_left) = g.reset()

done = False
while not done:
    action = strategy(n_heads, n_tails, flips_left)
    (n_heads, n_tails, flips_left), reward, done, info = g.step(action)
```	

To use the browser interaction environment you first need to install [FireFox](https://www.mozilla.org/en-US/firefox/new/), [geckodriver](https://github.com/mozilla/geckodriver/releases/).
You then change the file paths in `game_browser.py` to use your files by changing `geckodriver_path`.

The browser interaction environment can then be used with the same [gym](https://github.com/openai/gym/) API:

```python
from game_browser import CoinGameBrowser

def strategy(n_heads, n_tails, flips_left):
    # define your strategy here
    # see game.py for more details
    return 

g = CoinGameBrowser()

(n_heads, n_tails, flips_left) = g.reset()

done = False
while not done:
    action = strategy(n_heads, n_tails, flips_left)
    (n_heads, n_tails, flips_left), reward, done, info = g.step(action)
```	

## My highscore:

The highest score I have achieved was a 10+ hours overnight run with the following score:

<p align="center" title = "My highscore">
  <img src="assets/highscore.png" />
</p>
