"""Dynamic product-list interactions for Gajab category pages."""
from __future__ import annotations

import re
from dataclasses import dataclass

from framework.config.settings import settings
from framework.core.base_page import BasePage

BASE_URL = settings.base_url


@dataclass(frozen=True)
class ListedProduct:
    name: str
    price: int
    href: str


class GajabProductListPage(BasePage):
    TOYS_GAMES_PATH = "/product-list/toys-games/17?offset=0"
    BRAND_LOAD_MORE = "#brand-filter-load-more-btn"
    MIN_PRICE_RANGE = "#price-filter-website-min-range-input"
    MAX_PRICE_RANGE = "#price-filter-website-max-range-input"
    PRODUCT_LINKS = "a[href*='/product-detail/']"

    def open_toys_and_games(self) -> "GajabProductListPage":
        url = f"{BASE_URL.rstrip('/')}{self.TOYS_GAMES_PATH}"
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
        self.page.get_by_role("heading", name=re.compile("Toys & Games", re.IGNORECASE)).wait_for(
            state="visible", timeout=self.timeout
        )
        return self

    def _brand_label(self, brand_name: str):
        return self.page.locator("label").filter(has_text=re.compile(f"^{re.escape(brand_name)}$", re.IGNORECASE)).first

    def select_brand(self, brand_name: str) -> "GajabProductListPage":
        label = self._brand_label(brand_name)
        load_more = self.page.locator(self.BRAND_LOAD_MORE)
        for _ in range(5):
            if label.count():
                break
            if not load_more.count() or not load_more.is_visible():
                break
            load_more.click(force=True, timeout=self.timeout)
            label = self._brand_label(brand_name)

        if not label.count():
            raise AssertionError(f"Brand filter '{brand_name}' was not rendered")
        label.click(force=True, timeout=self.timeout)
        return self

    def _set_range_value(self, selector: str, value: int) -> None:
        slider = self.page.locator(selector)
        slider.wait_for(state="visible", timeout=self.timeout)
        slider.evaluate(
            """(element, desiredValue) => {
                const valueSetter = Object.getOwnPropertyDescriptor(
                    HTMLInputElement.prototype, 'value'
                ).set;
                valueSetter.call(element, String(desiredValue));
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
            }""",
            value,
        )

    def set_price_range(self, minimum: int, maximum: int) -> "GajabProductListPage":
        self._set_range_value(self.MIN_PRICE_RANGE, minimum)
        self._set_range_value(self.MAX_PRICE_RANGE, maximum)
        self.page.wait_for_timeout(500)
        return self

    @staticmethod
    def _price_from_text(text: str) -> int | None:
        match = re.search(r"₹\s*([\d,]+)", text)
        return int(match.group(1).replace(",", "")) if match else None

    def products(self) -> list[ListedProduct]:
        products: list[ListedProduct] = []
        seen: set[str] = set()
        links = self.page.locator(self.PRODUCT_LINKS)
        for index in range(links.count()):
            link = links.nth(index)
            href = link.get_attribute("href") or ""
            if not href or href in seen:
                continue
            seen.add(href)
            text = (link.inner_text(timeout=self.timeout) or "").strip()
            name = link.locator("p").first.inner_text(timeout=self.timeout).strip()
            price = self._price_from_text(text)
            if price is not None:
                products.append(ListedProduct(name=name, price=price, href=href))
        return products

    def select_product(self, product_name: str) -> None:
        product = self.page.get_by_role("link", name=re.compile(re.escape(product_name), re.IGNORECASE)).first
        product.wait_for(state="visible", timeout=self.timeout)
        product.click(timeout=self.timeout)
