import allure
import pytest
from pages.saucedemo.login_page import LoginPage
from core.common_test import run_accessibility_check

@allure.epic("Accessibility Testing")
@allure.feature("Login Page")
@pytest.mark.saucedemo
class TestLoginPage:
    def test_login_page_accessibility(self, page, test_config, only_critical, warn_only):
        login_page = LoginPage(page)
        login_page.load(test_config["base_url"])
        run_accessibility_check(page, "Login Page", test_config, only_critical, warn_only)