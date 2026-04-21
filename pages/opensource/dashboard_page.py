from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.dashboard_icon = "#app > div.oxd-layout.orangehrm-upgrade-layout > div.oxd-layout-navigation > aside > nav > div.oxd-sidepanel-body > ul > li:nth-child(2) > a > span"

    def go_to_dashboard(self):
        self.page.click(self.dashboard_icon)
        self.page.wait_for_load_state("networkidle")