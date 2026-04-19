import allure
import pytest
from pages.opensource.login_page import LoginPage
from pages.opensource.admin_page import AdminPage
from core.common_test import run_accessibility_check

@allure.epic("Accessibility Testing")
@allure.feature("Admin Page")
class TestAdminPage:
    def test_admin_page_accessibility(self, page, test_config, only_critical, warn_only):
        login_page = LoginPage(page)
        admin_page = AdminPage(page)

        login_page.load(test_config["base_url"])
        login_page.do_login(test_config["username"], test_config["password"])
        admin_page.go_to_admin()

        run_accessibility_check(page, "Admin Page", test_config, only_critical, warn_only)