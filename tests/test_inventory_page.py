import allure
import pytest
from pages.login_page import LoginPage
from core.common_test import run_accessibility_check

@allure.epic("Accessibility Testing")
@allure.feature("Inventory Page")
@pytest.mark.saucedemo
class TestInventoryPage:
    def test_inventory_page_accessibility(self, page, test_config, only_critical, warn_only):
        login_page = LoginPage(page)
        login_page.load(test_config["base_url"])
        login_page.do_login(test_config["username"], test_config["password"])

        run_accessibility_check(page, "Inventory Page", test_config, only_critical, warn_only)