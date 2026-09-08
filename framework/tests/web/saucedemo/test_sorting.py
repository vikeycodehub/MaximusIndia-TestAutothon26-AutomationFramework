"""
Regression test: product sorting must actually reorder items on screen.
Good example of a check that's tedious to verify manually every time but
trivial to automate.
"""
import allure
import pytest

from framework.pages.saucedemo.inventory_page import InventoryPage
from framework.pages.saucedemo.login_page import LoginPage


@allure.feature("SauceDemo - Sorting")
@pytest.mark.regression
@pytest.mark.web
def test_sort_price_low_to_high(page):
    login = LoginPage(page).open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.sort_by("lohi")
    prices = inventory.item_prices()

    assert prices == sorted(prices), f"Prices should be ascending, got: {prices}"


@allure.feature("SauceDemo - Sorting")
@pytest.mark.regression
@pytest.mark.web
def test_sort_price_high_to_low(page):
    login = LoginPage(page).open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.sort_by("hilo")
    prices = inventory.item_prices()

    assert prices == sorted(prices, reverse=True), f"Prices should be descending, got: {prices}"
