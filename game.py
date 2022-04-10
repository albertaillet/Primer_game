import io
import re
import time
import base64 
import numpy as np
from PIL import Image
import pytesseract as tess

tess.pytesseract.tesseract_cmd = "C:\\Users\\alber\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class CoinGame():

    def __init__(self, driver=None):
        driver_not_provided = (driver is None)
        if driver_not_provided:
            driver = self._get_driver()
            driver.get('https://primerlearning.org/')
        self.driver = driver
        self.element = self.driver.find_element_by_id("coin-flip-app")
        self.window_size = (300,850)
        self.reset_window()

        self.heads = None
        self.tails = None
        self.score = None
        self.flips_left = None
    
        self.re_heads = re.compile(r"(?<=Heads: )[\d]+")
        self.re_tails = re.compile(r"(?<=Tails: )[\d]+")
        self.re_score = re.compile(r"(?<=score: )[\d]+")
        self.re_flips_left = re.compile(r"[\d]+(?= Flips left)")
        
        if driver_not_provided:
            self._wait_for_loading()
            self.toggle_show_flipping_animations()
        
    def _wait_for_loading(self):
        progress = 0
        loaded = False
        while not loaded:
            screenshot = self.get_page_screenshot()

            loading_bar = screenshot.crop((224, 757, 500, 786))
            threshold = loading_bar.point(lambda p: 1 if p > 200 else 0)
            threshold = np.array(threshold)
            if threshold.sum()/threshold.size > progress:
                progress = threshold.sum()/threshold.size
            
            title = screenshot.crop((100, 70, 700, 400))
            title_text = CoinGame._get_image_text(title)
            if "Catch the cheaters!" in title_text:
                loaded = True
                progress = 1
            print(f"Loading: {100*progress:5.1f}%", end='\r')
            time.sleep(1)

    def _get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        mobile_emulation = { "deviceName": "iPhone 6" }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        return webdriver.Chrome(options= chrome_options)

    def reset_window(self):
        self.driver.set_window_size(*self.window_size)
        self.driver.execute_script("arguments[0].scrollIntoView();", self.element)

    def get_page_screenshot(self):
        self.reset_window()
        screenshot = self.driver.get_screenshot_as_base64()
        screenshot = base64.b64decode(screenshot)
        screenshot = io.BytesIO(screenshot)
        screenshot = Image.open(screenshot).convert('L')
        return screenshot

    @staticmethod
    def _get_image_text(image):
        return tess.image_to_string(image)

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
        screenshot = self.get_page_screenshot()

        crop = screenshot.crop((0, 490, 750, 985))
        text = CoinGame._get_image_text(crop)

        self.heads = self.parse_heads(text)
        self.tails = self.parse_tails(text)
        self.score = self.parse_score(text)
        self.flips_left = self.parse_flips_left(text)

        return {k:v for k, v in zip(["heads", "tails", "score", "flips_left"], [self.heads, self.tails, self.score, self.flips_left])}

    def parse_heads(self, string):
        m = self.re_heads.search(string)
        if m:
            return int(m.group(0))
        return 0

    def parse_tails(self, string):
        m = self.re_tails.search(string)
        if m:
            return int(m.group(0))
        return 0

    def parse_flips_left(self, string):
        m = self.re_flips_left.search(string)
        if m:
            return int(m.group(0))

    def parse_score(self, string):
        m = self.re_score.search(string.lower())
        if m:
            return int(m.group(0))

    def _click_location(self, x, y):
        self.reset_data()
        self.reset_window()
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.element, x, y)
        action.click()
        action.perform()
    
    # Clicking locations:
    # Game: x, y = 20, 20
    # Leaderboard x, y = 330, 20
    # 1 Coin: x, y = 20, 500
    # 5 Coins: x, y = 330, 500
    # Show flipping animation: x, y = 50, 550
    # Fair: x, y = 20, 600
    # Cheater x, y = 330, 600
    # Reset Game: x, y = 155, 600

    def click_game_tab(self):
        self._click_location(20, 20)

    def click_leaderboard_tab(self):
        self._click_location(330, 20)

    def flip_one_coin(self):
        self._click_location(20, 500)
    
    def flip_five_coins(self):
        self._click_location(330, 500)
    
    def toggle_show_flipping_animations(self):
        self._click_location(50, 550)
    
    def label_fair(self):
        self._click_location(20, 600)

    def label_cheater(self):
        self._click_location(330, 600)

    def reset_game(self):
        self._click_location(155, 600)
        self.reset_window()
    
    def restart_browser(self):
        self.driver.quit()
        self.__init__()