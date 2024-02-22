
class Base_Page:
    def __init__(self, driver):
        self._driver = driver

    def get_page_title(self):
        return self._driver.title
