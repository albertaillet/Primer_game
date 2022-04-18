"""
 Albert Aillet, April 2022
Makes use of the CoinGame class and the Primer website 
https://primerlearning.org/ from the YouTube channel
Primer: https://www.youtube.com/channel/UCKzJFdi57J53Vr_BkTfN3uQ

Used the following thread to resolve ActionChain issue:
https://stackoverflow.com/questions/67614276/perform-and-reset-actions-in-actionchains-not-working-selenium-python
"""
import io, time
import numpy as np
from PIL import Image, ImageOps

game_website_link = 'https://primerlearning.org/'
geckodriver_path = r"C:\Users\alber\Documents\My_Code\Primer_game\geckodriver.exe"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from game import CoinGame


class CoinGameBrowser(CoinGame):

    def __init__(self, 
                 driver=None,
                 window_size = (465,820),
                 label_animation_time = 1.3,
                 game_over_animate_time = 3.0,
                 ):
        
        driver_not_provided = (driver is None)
        if driver_not_provided:
            driver = CoinGameBrowser.get_driver()

        self.driver = driver
        self.window_size = window_size
        self.label_animation_time = label_animation_time
        self.done_animation_time = game_over_animate_time
        self.reset_window()

        super().__init__()

        self.element = self.driver.find_element_by_id("coin-flip-app")
        self.action_chain = ActionChains(self.driver)
    
        self.clicking_locations = {
            "flip_one": (250, 1050),
            "flip_five": (500, 1050),
            "toggle_show_flipping_animations": (360, 1150),
            "label_fair": (250, 1200),
            "label_cheater": (500, 1200),
            "reset": (360, 1200),
        }

        if driver_not_provided:
            self._wait_for_loading()
            time.sleep(2) # wait for starting animation to finish
        
        self.reset_values()
        self.toggle_show_flipping_animations()
    
    def reset_values(self):
        self.heads = 0
        self.tails = 0
        self.score = 0
        self.flips_left = 100
        self.done = False
        self.initial_flip = True
        self.last_action = None
        self.crop_heads, self.crop_tails, self.crop_score = self.get_page_crops()
        
    def _wait_for_loading(self):
        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)
        WebDriverWait(self.driver, 200).until(
            lambda drvr: drvr.find_element_by_id("unity-progress-bar-full")
                             .get_attribute("style") == "width: 100%;")
        self.driver.switch_to.default_content()

    @staticmethod
    def get_driver():
        # Get the Firefox driver and load the game website.
        driver = webdriver.Firefox(executable_path=geckodriver_path)
        driver.get(game_website_link)

        # Set correct zoom level.
        driver.set_context("chrome") 
        win = driver.find_element_by_tag_name("body")
        for _ in range(4):
            win.send_keys(Keys.CONTROL, "-")
        driver.set_context("content")
        driver.set_window_position(-5, 0, windowHandle ='current')
        return driver

    def reset_window(self):
        self.driver.set_window_size(*self.window_size)
        self.driver.execute_script("scroll(0, -250);")

    def get_page_screenshot(self):
        self.reset_window()
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = io.BytesIO(screenshot)
        screenshot = Image.open(screenshot).convert('L')
        screenshot = ImageOps.invert(screenshot)
        return screenshot

    def get_page_crops(self):
        screenshot = self.get_page_screenshot()
        # crop both tails and heads: (505, 810, 860, 910)
        crop_score = screenshot.crop((120, 1370, 400, 1410))
        crop_heads = screenshot.crop((505, 810, 860, 850))
        crop_tails = screenshot.crop((505, 870, 860, 910))
        return crop_heads, crop_tails, crop_score

    def observe(self) -> tuple:  
        return self.heads, self.tails, self.flips_left

    def _update_data(self):
        crop_heads, crop_tails, crop_score = self.get_page_crops()

        if self.last_action == "flip":
            heads_changed = crop_heads != self.crop_heads
            tails_changed = crop_tails != self.crop_tails
            if heads_changed and not tails_changed:
                self.heads += 1
            elif tails_changed and not heads_changed:
                self.tails += 1
            elif heads_changed and tails_changed and self.initial_flip:
                # hack to find if the initial flip was heads or tails.
                # if heads = 0 and tails = 1 sum is 79,055 and 170,932
                # if heads = 1 and tails = 0 sum is 99,266 and 153,675 
                sum_heads = (np.array(crop_heads).sum() - 2500000) / 1000
                sum_tails = (np.array(crop_tails).sum() - 2500000) / 1000
                if 78 < sum_heads < 80 and 170 < sum_tails < 172:
                    self.tails += 1
                elif 98 < sum_heads < 100 and 153 < sum_tails < 154:
                    self.heads += 1
                else:
                    raise ValueError(f"Unknown flip, {sum_heads}, {sum_tails}")
        elif self.last_action == "label": 
            score_changed = crop_score != self.crop_score
            if score_changed:
                self.score += 1
                self.flips_left += 15
            else:
                self.flips_left -= 30
                if self.flips_left < 0:
                    self.done = True
        
        self.crop_score = crop_score
        self.crop_heads = crop_heads
        self.crop_tails = crop_tails

    def _click_location(self, x, y):
        (self.action_chain.move_to_element_with_offset(self.element, x, y)
                          .click()
                          .perform())
        self.action_chain.reset_actions()
        for device in self.action_chain.w3c_actions.devices:
            device.clear_actions()
        if (self.heads == 0 and self.tails == 0) or self.last_action=="label":
            time.sleep(self.label_animation_time)

    def flip_one_coin(self):
        self.last_action = "flip"
        if (not self.done) and (self.flips_left > 0):
            self._click_location(*self.clicking_locations["flip_one"])
            self.flips_left -= 1
        self._update_data()
    
    def flip_five_coins(self):
        for _ in range(5):
            self.flip_one_coin()
    
    def toggle_show_flipping_animations(self):
        if not self.done:
            self._click_location(*self.clicking_locations["toggle_show_flipping_animations"])
    
    def label_fair(self):
        self._label("label_fair")

    def label_cheater(self):
        self._label("label_cheater")

    def _label(self, label):
        self.last_action = "label"
        if not self.done:
            self._click_location(*self.clicking_locations[label])
            if self.flips_left <= 30:
                time.sleep(self.done_animation_time)
            else:
                time.sleep(self.label_animation_time)
            self._update_data()
            self.heads = 0
            self.tails = 0

    def reset_game(self):
        if self.done:
            self._click_location(*self.clicking_locations["reset"])
            self.reset_window()
            time.sleep(self.label_animation_time)
            self._update_data()
            self.reset_values()
    
    def restart_browser(self):
        self.driver.quit()
        self.__init__()