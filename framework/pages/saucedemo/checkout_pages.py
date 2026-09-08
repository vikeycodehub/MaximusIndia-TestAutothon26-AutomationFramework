"""Checkout flow: step one (info) -> step two (overview) -> complete."""
from __future__ import annotations

from framework.core.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    ERROR_MESSAGE = "h3[data-test='error']"

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTAL_CODE, postal_code)

    def continue_to_overview(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)

    def error_text(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)


class CheckoutStepTwoPage(BasePage):
    TOTAL_LABEL = ".summary_total_label"
    FINISH_BUTTON = "#finish"

    def total_text(self) -> str:
        return self.text_of(self.TOTAL_LABEL)

    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = ".complete-header"

    def header_text(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)

    def is_order_complete(self) -> bool:
        return self.is_visible(self.COMPLETE_HEADER)
