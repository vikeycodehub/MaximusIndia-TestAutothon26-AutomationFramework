"""Product listing ("Products") screen after a successful login."""
from __future__ import annotations

from framework.core.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_IMG = ".inventory_item_img img"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    SORT_DROPDOWN = "[data-test='product-sort-container']"

    def is_loaded(self) -> bool:
        return self.is_visible(self.PAGE_TITLE)

    def add_to_cart_by_product_id(self, product_slug: str) -> "InventoryPage":
        """product_slug example: 'sauce-labs-backpack' -> button id add-to-cart-sauce-labs-backpack"""
        self.click(f"#add-to-cart-{product_slug}")
        return self

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def item_prices(self) -> list[float]:
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def item_image_sources(self) -> list[str]:
        return self.page.locator(self.ITEM_IMG).evaluate_all(
            "els => els.map(e => e.getAttribute('src'))"
        )

    def sort_by(self, option_value: str) -> None:
        """option_value one of: az, za, lohi, hilo"""
        self.page.locator(self.SORT_DROPDOWN).select_option(option_value)
