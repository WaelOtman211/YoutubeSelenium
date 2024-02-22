import time
from telnetlib import EC

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from infra.base_page import Base_Page

"""
With these methods, i can perform various actions that are commonly part of usability testing scenarios,
such as searching for a video, playing a video,skip advertising that's appear on the video ,
adjusting settings like volume and playback speed,
enabling closed captions, and navigating to different sections of the application like the channels page.
"""


class VideoUsability(Base_Page):
    SEARCH_INPUT = "//input[@id='search']"
    FIRST_VIDEO = "(//ytd-video-renderer)[1]"
    PLAY_BUTTON = "//button[@title='Play'] "
    PAUSE_BUTTON = "//button[@aria-label='Pause']"
    VOLUME_SLIDER = "//div[@aria-label='Volume']"
    VOLUME_BUTTON="(//button[@class='ytp-mute-button ytp-button'])[1]"
    PLAYBACK_SPEED_MENU = "(//div[@class='ytp-menuitem-label'])[3]"
    CC_BUTTON = "//button[@title='Subtitles/closed captions (c)']"
    CHANNEL_BUTTON = "//yt-formatted-string[text()='Channels']"
    VIDEO_ELEMENT = "//video[@class='video-stream']"
    SKIP_BUTTON = "//button[@class='ytp-ad-skip-button-modern ytp-button']"
    SETTING_BUTTON="(//button[@title='Settings'])[1]"
    PLAYBACK_SPEED_OPTION = "(//div[@class='ytp-popup ytp-settings-menu'])[1]"

    def search_for_video(self, keyword):
        # Type the search keyword into the search input field
        search_input = self._driver.find_element(By.XPATH, self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)

    def play_first_video(self):
        try:
            first_video = self._driver.find_element(By.XPATH, self.FIRST_VIDEO)
            first_video.click()
        except Exception as e:
            print("Error selecting first video:", str(e))

    def hover_over_volume_slider(self):
        # Hover over the volume slider
        volume_button = self._driver.find_element(By.XPATH, self.VOLUME_BUTTON)
        action_chains = ActionChains(self._driver)
        action_chains.move_to_element(volume_button).perform()

    def adjust_volume(self, volume):
        # Adjust the volume level using the volume slider
        self.hover_over_volume_slider()
        volume_slider = self._driver.find_element(By.XPATH, self.VOLUME_SLIDER)
        current_volume = int(volume_slider.get_attribute("aria-valuenow"))
        offset = current_volume-volume

        ActionChains(self._driver).click_and_hold(volume_slider).move_by_offset(0, offset).release().perform()

    def click_setting_button(self):
        setting_button= self._driver.find_element(By.XPATH,self.SETTING_BUTTON)
        setting_button.click()

    def is_skip_button_present(self, xpath):
        try:
            skip_button = self._driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def click_skip_button(self, xpath):
        skip_button = self._driver.find_element(By.XPATH, xpath)
        skip_button.click()

    def adjust_playback_speed(self):
        # Select the playback speed from the playback speed menu
        skip_button_present = self.is_skip_button_present(self.SKIP_BUTTON)
        if skip_button_present:
            print("Skip button found. Clicking on skip button to start the video.")
            self.click_skip_button(self.SKIP_BUTTON)
        time.sleep(2)
        self.click_setting_button()
        time.sleep(2)
        playback_speed_menu = self._driver.find_element(By.XPATH, self.PLAYBACK_SPEED_MENU)
        playback_speed_menu.click()
        time.sleep(2)
        playback_speed_option = self._driver.find_element(By.XPATH, self.PLAYBACK_SPEED_OPTION)
        playback_speed_option.click()

    def enable_closed_captions(self):
        # Enable closed captions for the video
        cc_button = self._driver.find_element(By.XPATH, self.CC_BUTTON)
        cc_button.click()

    def go_to_channels_page(self):
        try:
            # Wait for the Channels button to be clickable
            channel_button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.CHANNEL_BUTTON))
            )
            # Once clickable, click on the Channels button
            channel_button.click()
        except Exception as e:
            print("Error while navigating to channels page:", str(e))


