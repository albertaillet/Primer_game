## Primer game

This is a repository for my strategies to the game: [Coin Flip Cheaters: A game from Primer](https://www.youtube.com/watch?v=QC91Bf8hQVo).

`game.py` includes the class `CoinGame` that uses the openai [gym](https://github.com/openai/gym/) base class to set up the environment.

`game_browser.py` includes the class `CoinGameBrowser` that builds on `CoinGame` and iteracts with the online game at [primerlearning.org](https://primerlearning.org/).

`game_simulation.py` includes the class `CoinGameSimulation` that builds on `CoinGame` and implements a simulation of the game to test out the your strategies or models.

## How to use:

Start with creating the correct conda environment:

```bash
conda env create -f environment.yml
```

To use the simulation here is an example, the simulation uses [gym](https://github.com/openai/gym/) API model:

```python
from game_simulation import CoinGameSimulation

def strategy(n_heads, n_tails, flips_left):
    # define your strategy here
    # see game.py for more details
    return 

g = CoinGameSimulation()

(n_heads, n_tails, flips_left), info = g.reset(return_info=True)
done = False
while not done:
    action = strategy(n_heads, n_tails, flips_left)
    (n_heads, n_tails, flips_left), reward, done, info = g.step(action)
```	

To use the brower interaction environment you first need to install [FireFox](https://www.mozilla.org/en-US/firefox/new/), [geckodriver](https://github.com/mozilla/geckodriver/releases/) and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/releases).
You then change the file paths in `game_browser.py` to use the files by changing `geckodriver_path` and `tess.pytesseract.tesseract_cmd`.

The browser interaction environment can then be with the same [gym](https://github.com/openai/gym/) API model:

```python
from game_browser import CoinGameBrowser

def strategy(n_heads, n_tails, flips_left):
    # define your strategy here
    # see game.py for more details
    return 

g = CoinGameBrowser()

(n_heads, n_tails, flips_left), info = g.reset(return_info=True)
done = False
while not done:
    action = strategy(n_heads, n_tails, flips_left)
    (n_heads, n_tails, flips_left), reward, done, info = g.step(action)
```	

The notification sound used is taken from
[mixkit.co](https://mixkit.co/free-sound-effects/coin/) 
under the name *Coin win notification*.