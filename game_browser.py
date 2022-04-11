import io, re, time
from PIL import Image
import pytesseract as tess
from game import CoinGame

chromedirver_path = "C:\\Users\\alber\\Documents\\My_Code\\Python_sandbox\\Primer_game\\chromedriver.exe"
tess.pytesseract.tesseract_cmd = "C:\\Users\\alber\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

class CoinGameBrower(CoinGame):

    def __init__(self, 
                 driver=None,
                 window_size = (300,850),
                 label_animation_time = 1.3):
        
        driver_not_provided = (driver is None)
        if driver_not_provided:
            driver = self._get_driver()
            driver.get('https://primerlearning.org/')
        
        self.driver = driver
        self.element = self.driver.find_element_by_id("coin-flip-app")
        self.window_size = window_size
        self.reset_window()

        self.label_animation_time = label_animation_time

        self.heads = None
        self.tails = None
        self.score = None
        self.flips_left = None

        self.game_over = False
        self.outdated_data = True
    
        self.re_heads = re.compile(r"(?<=Heads: )[\d]+")
        self.re_tails = re.compile(r"(?<=Tails: )[\d]+")
        self.re_score = re.compile(r"(?<=score: )[\d]+")
        self.re_flips_left = re.compile(r"[\d]+(?= Flips left)")

        self.clicking_locations = {
            "flip_one": (20, 500),
            "flip_five": (330, 500),
            "toggle_show_flipping_animations": (50, 550),
            "label_fair": (20, 600),
            "label_cheater": (330, 600),
            "reset": (155, 600),
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

    def _get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        mobile_emulation = { "deviceName": "iPhone 6" }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        return webdriver.Chrome(executable_path=chromedirver_path, options= chrome_options)

    def reset_window(self):
        self.driver.set_window_size(*self.window_size)
        self.driver.execute_script("arguments[0].scrollIntoView();", self.element)

    def get_page_screenshot(self):
        self.reset_window()
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = io.BytesIO(screenshot)
        screenshot = Image.open(screenshot).convert('L')
        return screenshot

    @staticmethod
    def _get_image_text(image):
        return tess.image_to_string(image)

    def get_data(self) -> dict: 
        if self.outdated_data or any(val is None for val in [self.heads, self.tails, self.score, self.flips_left]):
            self._update_data()

        return {k:v for k, v in zip(["heads", "tails", "score", "flips_left"], 
                                    [self.heads, self.tails, self.score, self.flips_left])}

    def _update_data(self):
        screenshot = self.get_page_screenshot()

        crop = screenshot.crop((0, 490, 750, 985))
        text = CoinGameBrower._get_image_text(crop)

        self.game_over = "the leaderboard" in text.lower() or "game over" in text.lower()

        self.heads = self.parse_heads(text)
        self.tails = self.parse_tails(text)
        self.score = self.parse_score(text)
        self.flips_left = self.parse_flips_left(text)

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
        self.outdated_data = True
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.element, x, y)
        action.click()
        action.perform()    
        if self.heads == 0 and self.tails == 0:
            time.sleep(self.label_animation_time)

    def flip_one_coin(self):
        if not self.game_over and self.flips_left > 0:
            self._click_location(*self.clicking_locations["flip_one"])
    
    def flip_five_coins(self):
        if not self.game_over and self.flips_left > 0:
            self._click_location(*self.clicking_locations["flip_five"])
    
    def toggle_show_flipping_animations(self):
        if not self.game_over:
            self._click_location(*self.clicking_locations["toggle_show_flipping_animations"])
    
    def label_fair(self):
        if not self.game_over:
            self._click_location(*self.clicking_locations["label_fair"])
            time.sleep(self.label_animation_time)

    def label_cheater(self):
        if not self.game_over:
            self._click_location(*self.clicking_locations["label_cheater"])
            time.sleep(self.label_animation_time)

    def reset_game(self):
        if self.game_over:
            self._click_location(*self.clicking_locations["reset"])
            self.reset_window()
            self.game_over = False
    
    def restart_browser(self):
        self.driver.quit()
        self.__init__()