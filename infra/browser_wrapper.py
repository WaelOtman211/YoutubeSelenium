from selenium import webdriver


class Browser_Wrapper:
    def __init__(self):
        self.driver = None
        print("test Start")

    def get_driver(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        return self.driver
