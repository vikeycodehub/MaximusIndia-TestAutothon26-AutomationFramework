"""Flow 02: pincode selection and dynamic home-page product intelligence."""
from __future__ import annotations

import pytest

from framework.pages.gajab.home_page import GajabHomePage


@pytest.mark.web
@pytest.mark.smoke
def test_pincode_is_reflected_in_header(page):
    home_page = GajabHomePage(page).open()

    home_page.set_pincode("560037")

    assert "560037" in home_page.current_location_text()


@pytest.mark.web
@pytest.mark.smoke
def test_home_sections_return_dynamic_products(page):
    home_page = GajabHomePage(page).open()

    deal = home_page.deal_of_the_day()
    most_bargained = home_page.most_bargained_trending_product()
    cheapest = home_page.cheapest_just_bargained_product()

    assert deal.name and deal.asking_price is not None
    assert deal.href.startswith("/product-detail/")
    assert most_bargained.name and most_bargained.bargains is not None
    assert most_bargained.href.startswith("/product-detail/")
    assert cheapest.name and cheapest.asking_price is not None
    assert cheapest.href.startswith("/product-detail/")
