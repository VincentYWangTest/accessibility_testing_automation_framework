from datetime import datetime
import os

class Utils:
    @staticmethod
    def wait_for_element(page, locator, timeout=60000):
        try:
            page.wait_for_selector(locator, state="visible", timeout=timeout)
            return True
        except Exception as e:
            print(f"[ERROR] Element not found: {locator}, {str(e)}")
            return False

    @staticmethod
    def take_screenshot(page, page_name, suffix="fail"):
        os.makedirs("screenshots", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{page_name}_{suffix}_{ts}.png"
        page.screenshot(path=path, full_page=True)
        return path

    @staticmethod
    def switch_to_iframe(page, locator):
        if Utils.wait_for_element(page, locator):
            page.frame_locator(locator).locator("body").wait_for()
            return True
        return False

    @staticmethod
    def switch_to_default(page):
        page.frame_locator("body").locator("body").wait_for()