from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from infra.base_page import Base_Page
import time


class VideoPage(Base_Page):
    SEARCH_INPUT = "//input[@id='search']"
    FIRST_VIDEO = "(//ytd-video-renderer)[1]"
    CC_BUTTON = "//button[@title='Subtitles/closed captions (c)']"  # Update with the actual XPath of the CC button
    CLOSED_CAPTIONS_TEXT = "//span[@class='captions-text']"  # Update with the actual XPath of the closed captions text
    HOME_BUTTON = "//yt-icon[@id='logo-icon']"  # Update with the actual XPath of the home button
    HISTORY_BUTTON = "//a[@title='History']"  # Update with the actual XPath of the history button
    # Update with the actual XPath of the last watched video title
    LAST_WATCHED_VIDEO_TITLE = "(//a[@class='yt-simple-endpoint style-scope ytd-video-renderer'])[1]"
    NEXT_VIDEO_CSS = ".ytp-button.ytp-next-button"
    SKIP_BUTTON = "//button[@class='ytp-ad-skip-button-modern ytp-button']"

    def __init__(self, driver):
        super().__init__(driver)
        self.search_ipnut = self._driver.find_element(By.XPATH, self.SEARCH_INPUT)

    def fill_search_input(self, text):
        self.search_ipnut.send_keys(text)

    def press_enter_on_search_input(self):
        self.search_ipnut.send_keys(Keys.RETURN)

    def search_flow(self, text):
        self.fill_search_input(text)
        self.press_enter_on_search_input()

    def choose_first_video(self):
        try:
            first_video = self._driver.find_element(By.XPATH, self.FIRST_VIDEO)
            first_video.click()
        except Exception as e:
            print("Error selecting first video:", str(e))

    def is_video_muted(self):
        try:
            video_element = self._driver.find_element(By.TAG_NAME, 'video')
            return video_element.get_attribute('muted') == 'true'
        except Exception as e:
            print("Error getting video mute status:", str(e))
            return False

    def the_routine_flow(self,text):
        self.search_flow(text)
        time.sleep(5)  # Adjust wait time as needed
        self.choose_first_video()
        time.sleep(5)  # Adjust wait time as needed

    def mute_video_flow(self, text):
        self.the_routine_flow(text)
        print("the result is",self.is_video_muted())
        return self.is_video_muted()

    def enable_closed_captions(self):
        try:
            cc_button = self._driver.find_element(By.XPATH, self.CC_BUTTON)
            cc_button.click()
        except Exception as e:
            print("Error enabling closed captions:", str(e))

    def is_closed_captions_visible(self):
        try:
            closed_captions_text = self._driver.find_element(By.XPATH, self.CLOSED_CAPTIONS_TEXT)
            return closed_captions_text.is_displayed()
        except Exception as e:
            print("Error checking visibility of closed captions:", str(e))
            return False

    def go_to_home_page(self):
        home_button = self._driver.find_element(By.XPATH, self.HOME_BUTTON)
        home_button.click()

    def go_to_history_page(self):
        history_button = self._driver.find_element(By.XPATH, self.HISTORY_BUTTON)
        history_button.click()

    def get_last_watched_video_title(self):
        last_watched_video_title = self._driver.find_element(By.XPATH, self.LAST_WATCHED_VIDEO_TITLE).text
        return last_watched_video_title

    def check_last_watched_video_in_history(self,text):
        self.the_routine_flow(text)
        self.go_to_home_page()
        time.sleep(5)  # Adjust wait time as needed
        self.go_to_history_page()
        time.sleep(5)  # Adjust wait time as needed
        last_watched_video_title = self.get_last_watched_video_title()
        return last_watched_video_title

    def is_skip_button_present(self, xpath):
        try:
            skip_button = self._driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def click_skip_button(self, xpath):
        skip_button = self._driver.find_element(By.XPATH, xpath)
        skip_button.click()

    def check_closed_captions_visibility(self,text):
        self.the_routine_flow(text)
        self.enable_closed_captions()
        time.sleep(5)  # Adjust wait time as needed
        return self.is_closed_captions_visible()

    def click_to_the_next_video(self,text):
        self.the_routine_flow(text)
        next_video_button = self._driver.find_element(By.CSS_SELECTOR, self.NEXT_VIDEO_CSS)
        next_video_button.click()
        time.sleep(3)
        next_video_button.click()
        time.sleep(5)
        skip_button_present = self.is_skip_button_present(self.SKIP_BUTTON)
        if skip_button_present:
            print("Skip button found. Clicking on skip button to start the video.")
            self.click_skip_button(self.SKIP_BUTTON)
        return self.is_video_playing()

    def is_video_playing(self):
        # Check if the video is playing by inspecting the player's state
        return self._driver.execute_script("return document.getElementById('movie_player').getPlayerState()") == 1

