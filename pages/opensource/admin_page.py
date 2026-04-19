from pages.base_page import BasePage

class AdminPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.admin_icon = "#app > div.oxd-layout.orangehrm-upgrade-layout > div.oxd-layout-navigation > aside > nav > div.oxd-sidepanel-body > ul > li:nth-child(1) > a > span"

    def go_to_admin(self):
        self.page.click(self.admin_icon)
        self.page.wait_for_load_state("networkidle")