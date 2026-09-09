"""Executable matrix for Gajab checks currently backed by verified page objects.

Cases that require an email inbox, payment provider, Android device, visual
baseline, or security tooling remain in the manual matrix and are reported as
MANUAL_REQUIRED rather than being represented by false-positive tests.
"""
from __future__ import annotations

import random

import pytest

from framework.pages.gajab.home_page import GajabHomePage
from framework.pages.gajab.login_page import GajabLoginPage
from framework.pages.gajab.product_list_page import GajabProductListPage


REQUIRED_PRODUCT = "Classic 15.7 Inch Soft Tip Dartboard Game Set"


@pytest.mark.web
@pytest.mark.critical
@pytest.mark.parametrize("case_id", ["GJ-MAN-001"], ids=["GJ-MAN-001-login-otp"])
def test_automated_authentication_flow(page, case_id):
    mobile = "9" + "".join(str(random.randint(0, 9)) for _ in range(9))
    login = GajabLoginPage(page).open()
    login.login_with_mobile(mobile)
    assert login.is_logged_in(), f"{case_id}: login did not reach authenticated state"


@pytest.mark.web
@pytest.mark.parametrize("case_id,pincode", [("GJ-MAN-005", "560037")], ids=["GJ-MAN-005-pincode"])
def test_automated_location_flow(page, case_id, pincode):
    home = GajabHomePage(page).open()
    home.set_pincode(pincode)
    assert pincode in home.current_location_text(), f"{case_id}: pincode not reflected"


@pytest.mark.web
@pytest.mark.parametrize(
    "case_id",
    ["GJ-MAN-007", "GJ-MAN-008", "GJ-MAN-010"],
    ids=["GJ-MAN-007-deal", "GJ-MAN-008-trending", "GJ-MAN-010-cheapest"],
)
def test_automated_dynamic_home_sections(page, case_id):
    home = GajabHomePage(page).open()
    if case_id == "GJ-MAN-007":
        product = home.deal_of_the_day()
        assert product.name and product.asking_price is not None and product.href.startswith("/product-detail/")
    elif case_id == "GJ-MAN-008":
        product = home.most_bargained_trending_product()
        assert product.name and product.bargains is not None and product.href.startswith("/product-detail/")
    else:
        product = home.cheapest_just_bargained_product()
        assert product.name and product.asking_price is not None and product.href.startswith("/product-detail/")


@pytest.mark.web
@pytest.mark.critical
def test_automated_product_filter_flow(page):
    product_list = GajabProductListPage(page).open_toys_and_games()
    product_list.select_brand("SERA'S BASKET")
    product_list.set_price_range(427, 727)
    products = [
        product for product in product_list.products()
        if REQUIRED_PRODUCT.lower() in product.name.lower()
    ]
    assert products, "GJ-MAN-014: required product not found after filters"
    assert all(427 <= product.price <= 727 for product in products), "GJ-MAN-013: product outside price range"
    product_list.select_product(REQUIRED_PRODUCT)
    assert "/product-detail/" in page.url, "GJ-MAN-040: product detail did not open"
