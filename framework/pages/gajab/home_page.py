"""
Home page header controls (location/pincode picker, category nav) for Gajab.

Selectors verified live against the staging site on 2026-09-09.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from framework.core.base_page import BasePage

BASE_URL = "https://stg.gajab.com/"


@dataclass(frozen=True)
class GajabProduct:
    name: str
    asking_price: int | None
    bargains: int | None
    href: str
    image_url: str | None = None


class GajabHomePage(BasePage):
    LOCATION_MENU_BTN = "#location-desktop-menu-btn"
    LOCATION_MENU_TEXT = "#location-desktop-menu-text"
    PINCODE_INPUT = "#location-desktop-search-input"
    PINCODE_SUGGESTION = "#location-desktop-suggestion-item-0"
    DEAL_OF_THE_DAY_HEADING = "text=Gajab Deal Of The Day"
    TRENDING_HEADING = "text=Trending"
    JUST_BARGAINED_HEADING = "text=Just Bargained"

    def open(self) -> "GajabHomePage":
        self.goto(BASE_URL)
        return self

    def set_pincode(self, pincode: str) -> "GajabHomePage":
        self.page.locator(self.LOCATION_MENU_BTN).first.click(force=True, timeout=self.timeout)
        self.page.locator(self.PINCODE_INPUT).fill(pincode, timeout=self.timeout)
        self.page.locator(self.PINCODE_SUGGESTION).click(force=True, timeout=self.timeout)
        return self

    def current_location_text(self) -> str:
        return self.page.locator(self.LOCATION_MENU_TEXT).first.text_content(timeout=self.timeout) or ""

    def open_category(self, category_name: str) -> None:
        self.page.locator(f"a:has-text('{category_name}')").first.click(timeout=self.timeout)

    @staticmethod
    def _price_from_text(text: str) -> int | None:
        match = re.search(r"₹\s*([\d,]+)", text)
        return int(match.group(1).replace(",", "")) if match else None

    @staticmethod
    def _bargains_from_text(text: str) -> int | None:
        match = re.search(r"([\d,]+)\s*Times Bargained", text, re.IGNORECASE)
        return int(match.group(1).replace(",", "")) if match else None

    def _section(self, heading_text: str):
        heading = self.page.get_by_role("heading", name=re.compile(heading_text, re.IGNORECASE)).first
        heading.wait_for(state="visible", timeout=self.timeout)
        return heading.locator("xpath=../..").first

    def _products_in_section(self, heading_text: str) -> list[GajabProduct]:
        section = self._section(heading_text)
        links = section.locator("a[href*='/product-detail/']")
        products: list[GajabProduct] = []
        seen_hrefs: set[str] = set()

        for index in range(links.count()):
            link = links.nth(index)
            href = link.get_attribute("href") or ""
            if not href or href in seen_hrefs:
                continue
            seen_hrefs.add(href)
            text = (link.inner_text(timeout=self.timeout) or "").strip()
            image = link.locator("img").first
            image_url = image.get_attribute("src") if image.count() else None
            if not text and image.count():
                text = image.get_attribute("alt") or ""
            name = re.split(r"\s+Asking Price\s+₹", text, maxsplit=1, flags=re.IGNORECASE)[0].strip()
            products.append(
                GajabProduct(
                    name=name or href.rsplit("/", 1)[-1],
                    asking_price=self._price_from_text(text),
                    bargains=self._bargains_from_text(text),
                    href=href,
                    image_url=image_url,
                )
            )
        return products

    def deal_of_the_day(self) -> GajabProduct:
        products = self._products_in_section("Gajab Deal Of The Day")
        if not products:
            raise AssertionError("Deal of the Day product was not rendered")
        return products[0]

    def trending_products(self) -> list[GajabProduct]:
        products = self._products_in_section("Trending")
        if not products:
            raise AssertionError("Trending products were not rendered")
        return products

    def most_bargained_trending_product(self) -> GajabProduct:
        products = self.trending_products()
        ranked = [product for product in products if product.bargains is not None]
        if not ranked:
            raise AssertionError("Trending products did not expose bargain counts")
        return max(ranked, key=lambda product: product.bargains or 0)

    def just_bargained_products(self) -> list[GajabProduct]:
        return self._products_in_section("Just Bargained")

    def cheapest_just_bargained_product(self) -> GajabProduct:
        products = [product for product in self.just_bargained_products() if product.asking_price is not None]
        if not products:
            raise AssertionError("Just Bargained products did not expose asking prices")
        return min(products, key=lambda product: product.asking_price or 0)

    def open_just_bargained_view_all(self) -> None:
        section = self._section("Just Bargained")
        section.get_by_role("link", name="View All").click(timeout=self.timeout)
