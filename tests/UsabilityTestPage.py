import time
import unittest
from infra.browser_wrapper import Browser_Wrapper
from logic.youtube_video_usability import VideoUsability


class UsabilityTest(unittest.TestCase):

    def setUp(self):
        self.browser = Browser_Wrapper()
        self.driver = self.browser.get_driver("https://www.youtube.com")
        self.video_page = VideoUsability(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_usability_actions(self):
        # Search for a video
        self.video_page.search_for_video("Python Programming")
        time.sleep(5)  # Adjust wait time as needed
        # Play the first video
        self.video_page.play_first_video()
        time.sleep(10)  # Adjust wait time as needed
        # Adjust playback speed
        self.video_page.adjust_playback_speed()
        time.sleep(3)
        # Adjust volume level
        self.video_page.adjust_volume(20)  # Adjust to 50%
        time.sleep(5)
        # Enable closed captions
        self.video_page.enable_closed_captions()
        time.sleep(4)
        # Go to channels page
        self.video_page.go_to_channels_page()
        time.sleep(10)

