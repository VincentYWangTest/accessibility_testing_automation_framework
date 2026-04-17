import allure
import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from core.common_test import run_accessibility_check

@allure.epic("Accessibility Testing")
@allure.feature("Cart Page")
@pytest.mark.saucedemo
class TestCartPage:
    def test_cart_page_accessibility(self, page, test_config, only_critical, warn_only):
        login_page = LoginPage(page)
        cart_page = CartPage(page)

        login_page.load(test_config["base_url"])
        login_page.do_login(test_config["username"], test_config["password"])
        cart_page.go_to_cart()

        run_accessibility_check(page, "Cart Page", test_config, only_critical, warn_only)