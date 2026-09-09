"""
Gajab (Bargain Bazaar) - Automation Quest steps 1-5:
navigate -> Log in/Sign up -> mobile number + OTP -> verify login success ->
set pincode and verify it reflects in the header.

Selectors and flow verified live against https://stg.gajab.com/ (staging).
"""
import random

import pytest

from framework.pages.gajab.home_page import GajabHomePage
from framework.pages.gajab.login_page import GajabLoginPage
from framework.pages.gajab.product_list_page import GajabProductListPage


@pytest.fixture
def random_mobile_number() -> str:
    """Generate a syntactically valid 10-digit Indian mobile number for each run."""
    return "9" + "".join(str(random.randint(0, 9)) for _ in range(9))


def test_gajab_login_with_default_otp(page, random_mobile_number):
    login_page = GajabLoginPage(page).open()
    login_page.login_with_mobile(random_mobile_number)

    assert login_page.is_logged_in(), "Expected 'Log in / Sign up' link to disappear after successful OTP login"


def test_gajab_pincode_selection_reflects_in_header(page):
    home_page = GajabHomePage(page).open()
    home_page.set_pincode("560037")

    assert "560037" in home_page.current_location_text()


@pytest.mark.smoke
def test_gajab_home_dynamic_product_sections(page):
    home_page = GajabHomePage(page).open()

    deal = home_page.deal_of_the_day()
    assert deal.name
    assert deal.asking_price is not None
    assert deal.href.startswith("/product-detail/")

    most_bargained = home_page.most_bargained_trending_product()
    assert most_bargained.bargains is not None
    assert most_bargained.href.startswith("/product-detail/")

    cheapest = home_page.cheapest_just_bargained_product()
    assert cheapest.asking_price is not None
    assert cheapest.href.startswith("/product-detail/")


@pytest.mark.critical
def test_gajab_toys_games_filters_and_product(page):
    product_list = GajabProductListPage(page).open_toys_and_games()
    product_list.select_brand("SERA'S BASKET")
    product_list.set_price_range(427, 727)

    matching_products = [
        product
        for product in product_list.products()
        if "Classic 15.7 Inch Soft Tip Dartboard Game Set".lower() in product.name.lower()
    ]
    assert matching_products, "Required dartboard product was not available after filters"
    assert all(427 <= product.price <= 727 for product in matching_products)
    product_list.select_product("Classic 15.7 Inch Soft Tip Dartboard Game Set")
