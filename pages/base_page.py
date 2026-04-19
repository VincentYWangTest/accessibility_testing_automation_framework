from core.utils import Utils

class BasePage:
    def __init__(self, page):
        self.page = page
        self.utils = Utils

    def load(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        self.utils.wait_for_element(self.page, "body")

    def wait_for_element(self, locator, timeout=60000):
        return self.utils.wait_for_element(self.page, locator, timeout)

    def take_screenshot(self, suffix=""):
        return self.utils.take_screenshot(self.page, self.__class__.__name__, suffix)