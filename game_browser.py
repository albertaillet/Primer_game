"""
Albert Aillet, April 2022
Makes use of the CoinGame class and the Primer website 
https://primerlearning.org/ from the YouTube channel
Primer: https://www.youtube.com/channel/UCKzJFdi57J53Vr_BkTfN3uQ

Used the following thread to resolve ActionChain issue:
https://stackoverflow.com/questions/67614276/perform-and-reset-actions-in-actionchains-not-working-selenium-python
"""
import io, re, time
import pytesseract as tess
from PIL import Image, ImageOps

game_website_link = 'https://primerlearning.org/'
geckodriver_path = r"C:\Users\alber\Documents\My_Code\Primer_game\geckodriver.exe"
tess.pytesseract.tesseract_cmd = r"C:\Users\alber\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

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
                 mask_blob = False
                 ):
        
        driver_not_provided = (driver is None)
        if driver_not_provided:
            driver = CoinGameBrowser.get_driver()

        self.driver = driver
        self.window_size = window_size
        self.label_animation_time = label_animation_time
        self.done_animation_time = game_over_animate_time
        self.mask_blob = mask_blob

        super().__init__()

        self.element = self.driver.find_element_by_id("coin-flip-app")
        self.action_chain = ActionChains(self.driver)
        self.reset_window()

        self.heads = 0
        self.tails = 0
        self.score = 0
        self.flips_left = 100

        self.done = False
        self.outdated_data = True
    
        self.re_heads = re.compile(r"(?<=Heads: )[\d]+")
        self.re_tails = re.compile(r"(?<=Tails: )[\d]+")
        self.re_score = re.compile(r"(?<=score: )[\d]+")
        self.re_flips_left = re.compile(r"[\d]+(?= Flips left)")

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
        
        self.toggle_show_flipping_animations()
        self._update_data()
        
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

    @staticmethod
    def _get_image_text(image, **kwargs):
        return tess.image_to_string(image, **kwargs)

    def observe(self) -> tuple: 
        if self.outdated_data or any(val is None for val in (self.heads, self.tails, self.score, self.flips_left)):
            self._update_data()

        return self.heads, self.tails, self.flips_left

    def _update_data(self):
        old_heads = self.heads
        old_tails = self.tails
        old_score = self.score
        old_flips_left = self.flips_left

        tries = 0
        while tries < 3:
            screenshot = self.get_page_screenshot()

            crop = screenshot.crop((100, 800, 980, 1420))
            if self.mask_blob:
                blob_mask = Image.new('L', (120, 220), (205))
                crop.paste(blob_mask, (210, 0))

            text = CoinGameBrowser._get_image_text(crop, config="--psm 6 --oem 3")

            l = text.lower()
            self.done = "save your score to the leaderboard?" in l or "game over" in l

            new_heads = self.parse_heads(text)
            new_tails = self.parse_tails(text)
            new_score = self.parse_score(text)
            new_flips_left = self.parse_flips_left(text)
            
            if self.done:
                break

            if (new_heads is not None and
                new_tails is not None and
                new_score is not None and
                new_flips_left is not None and
                (new_heads-old_heads in (0, 1) or new_heads==0) and 
                (new_tails-old_tails in (0, 1) or new_tails==0) and
                new_score-old_score in (0, 1) and 
                new_flips_left-old_flips_left in (15, 0, -1, -30)):
                break
            
            tries += 1
        
        if tries == 3:
            print("Failed to read game data. heads {}->{}, tails {}->{}, score {}->{}, flips {}->{}".format(
                old_heads, new_heads, old_tails, new_tails, old_score, new_score, old_flips_left, new_flips_left))

        self.heads = new_heads if new_heads is not None else old_heads
        self.tails = new_tails if new_tails is not None else old_tails
        self.score = new_score if new_score is not None else old_score
        self.flips_left = new_flips_left if new_flips_left is not None else old_flips_left
        
        self.outdated_data = False

    def parse_heads(self, string) -> int:
        m = self.re_heads.search(string)
        if m:
            return int(m.group(0))
        return 0

    def parse_tails(self, string) -> int:
        m = self.re_tails.search(string)
        if m:
            return int(m.group(0))
        return 0

    def parse_flips_left(self, string) -> int:
        m = self.re_flips_left.search(string)
        if m:
            return int(m.group(0))

    def parse_score(self, string) -> int:
        m = self.re_score.search(string.lower())
        if m:
            return int(m.group(0))

    def _click_location(self, x, y):
        (self.action_chain.move_to_element_with_offset(self.element, x, y)
                          .click()
                          .perform())
        self.action_chain.reset_actions()
        for device in self.action_chain.w3c_actions.devices:
            device.clear_actions()
        if self.heads == 0 and self.tails == 0 and not self.outdated_data:
            time.sleep(self.label_animation_time)
        self.outdated_data = True

    def flip_one_coin(self):
        if (not self.done) and (self.flips_left > 0):
            self._click_location(*self.clicking_locations["flip_one"])
            self.flips_left -= 1
    
    def flip_five_coins(self):
        if (not self.done) and (self.flips_left >= 5):
            self._click_location(*self.clicking_locations["flip_five"])
            self.flips_left -= 5
    
    def toggle_show_flipping_animations(self):
        if not self.done:
            self._click_location(*self.clicking_locations["toggle_show_flipping_animations"])
    
    def label_fair(self):
        self._label("label_fair")

    def label_cheater(self):
        self._label("label_cheater")

    def _label(self, label):
        if not self.done:
            self._click_location(*self.clicking_locations[label])
            if self.flips_left <= 30:
                time.sleep(self.done_animation_time)
            else:
                time.sleep(self.label_animation_time)
            self.heads = 0
            self.tails = 0

    def reset_game(self):
        if self.done:
            self.heads = 0
            self.tails = 0
            self.score = 0
            self.flips_left = 100
            self._click_location(*self.clicking_locations["reset"])
            self.reset_window()
            self.done = False
            self.outdated_data = True
            time.sleep(self.label_animation_time)
            self._update_data()
    
    def restart_browser(self):
        self.driver.quit()
        self.__init__()