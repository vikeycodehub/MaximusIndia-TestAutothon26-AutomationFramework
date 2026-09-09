"""
Login screen of SauceDemo (Swag Labs) - https://www.saucedemo.com/

Demo app chosen because it's the industry-standard QA training app: it has
real e-commerce flows (login/browse/cart/checkout) AND intentionally seeded
bugs via special usernames (problem_user, error_user, visual_user, ...),
making it perfect for practicing BOTH automation tracks of the challenge:
Automation Quest (build robust flows) and Bug Quest (find real defects).
"""
from __future__ import annotations

from framework.core.base_page import BasePage

BASE_URL = "https://www.saucedemo.com/"


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "h3[data-test='error']"

    def open(self) -> "LoginPage":
        self.goto(BASE_URL)
        return self

    def login(self, username: str, password: str) -> None:
        self.smart_fill(self.USERNAME_INPUT, username, "the username input field")
        self.smart_fill(self.PASSWORD_INPUT, password, "the password input field")
        self.smart_click(self.LOGIN_BUTTON, "the green Login submit button")

    def error_text(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
