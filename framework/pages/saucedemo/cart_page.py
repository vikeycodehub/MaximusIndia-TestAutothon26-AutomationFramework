"""Shopping cart screen."""
from __future__ import annotations

from framework.core.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    CHECKOUT_BUTTON = "#checkout"

    def item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
