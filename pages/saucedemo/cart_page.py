from pages.saucedemo.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_icon = ".shopping_cart_link"

    def go_to_cart(self):
        self.page.click(self.cart_icon)
        self.page.wait_for_load_state("networkidle")