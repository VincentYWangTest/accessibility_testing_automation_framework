import allure
import pytest
from pages.opensource.login_page import LoginPage
from pages.opensource.dashboard_page import DashboardPage
from core.common_test import run_accessibility_check

@allure.epic("Accessibility Testing")
@allure.feature("Dashboard Page")
class TestDashboardPage:
    def test_dashboard_page_accessibility(self, page, test_config, only_critical, warn_only):
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        login_page.load(test_config["base_url"])
        login_page.do_login(test_config["username"], test_config["password"])
        dashboard_page.go_to_dashboard()

        run_accessibility_check(page, "Dashboard Page", test_config, only_critical, warn_only)