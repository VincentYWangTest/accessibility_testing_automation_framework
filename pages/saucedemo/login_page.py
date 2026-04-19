from pages.saucedemo.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"

    def do_login(self, username, password):
        self.wait_for_element(self.username_input)
        self.wait_for_element(self.password_input)
        self.wait_for_element(self.login_button)

        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)
        self.page.wait_for_url("**/inventory.html", timeout=10000)