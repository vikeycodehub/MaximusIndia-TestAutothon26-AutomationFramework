"""Flow 03: Toys & Games navigation, brand/price filters, and product selection."""
from __future__ import annotations

import pytest

from framework.pages.gajab.product_list_page import GajabProductListPage


REQUIRED_PRODUCT = "Classic 15.7 Inch Soft Tip Dartboard Game Set"


@pytest.mark.web
@pytest.mark.critical
def test_toys_games_filter_and_product_selection(page):
    product_list = GajabProductListPage(page).open_toys_and_games()

    product_list.select_brand("SERA'S BASKET")
    product_list.set_price_range(427, 727)
    matching_products = [
        product
        for product in product_list.products()
        if REQUIRED_PRODUCT.lower() in product.name.lower()
    ]

    assert matching_products, f"{REQUIRED_PRODUCT} was not available after applying filters"
    assert all(427 <= product.price <= 727 for product in matching_products)

    product_list.select_product(REQUIRED_PRODUCT)
    assert "/product-detail/" in page.url
