import unittest
from infra.browser_wrapper import Browser_Wrapper
from logic.vedio_page import VideoPage

"""
here i have create 4 tests for the video 
"""

class YoutubeVideoPageTest(unittest.TestCase):
    TEXT_TO_PUT_IN_INPUT="Python for Beginners - Learn Python in 1 Hour"

    def setUp(self):
        self.browser = Browser_Wrapper()
        self.driver = self.browser.get_driver("https://www.youtube.com")
        self.video_page = VideoPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_check_silence_audio_of_video(self):
        is_muted = self.video_page.mute_video_flow(self.TEXT_TO_PUT_IN_INPUT)
        print("is muted :",is_muted)
        # Assert if the video is muted
        self.assertFalse(is_muted, "The video is not muted.")

    def test_check_closed_captions_visibility(self):
        is_cc_visible = self.video_page.check_closed_captions_visibility(self.TEXT_TO_PUT_IN_INPUT)
        print("is_cc_visible :",is_cc_visible)
        self.assertTrue(is_cc_visible, "Closed captions text is not visible.")

    def test_navigate_videos(self):
        self.assertTrue(self.video_page.click_to_the_next_video(self.TEXT_TO_PUT_IN_INPUT), "Next video is not playing")

    def test_check_last_watched_video_in_history_without_signIn_to_youtube (self):
        last_watched_video_title = self.video_page.check_last_watched_video_in_history(self.TEXT_TO_PUT_IN_INPUT)
        # Replace with the expected title of the last watched video
        expected_video_title = ""
        self.assertEqual(last_watched_video_title, expected_video_title, "Last watched video is not added to history.")