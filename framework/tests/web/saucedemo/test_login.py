"""
Login test suite for SauceDemo - covers happy path + key negative/edge cases
in one data-driven test. This is the pattern to copy for tomorrow's real AUT.
"""
import allure
import pytest

from framework.core.utils import load_json_data
from framework.pages.saucedemo.inventory_page import InventoryPage
from framework.pages.saucedemo.login_page import LoginPage

login_cases = load_json_data("saucedemo_login_cases.json")


@allure.feature("SauceDemo - Login")
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.web
def test_standard_user_can_login(page):
    login = LoginPage(page).open()
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    assert inventory.is_loaded(), "Products page should load after valid login"


@allure.feature("SauceDemo - Login")
@pytest.mark.regression
@pytest.mark.web
@pytest.mark.parametrize("case", login_cases, ids=[c["note"] for c in login_cases])
def test_login_scenarios_data_driven(page, case):
    login = LoginPage(page).open()
    login.login(case["username"], case["password"])

    if case["should_login"]:
        inventory = InventoryPage(page)
        assert inventory.is_loaded(), f"Expected successful login for {case['username']}"
    else:
        assert login.has_error(), f"Expected an error message for case: {case['note']}"
        assert case["expected_error"] in login.error_text(), (
            f"Error text mismatch for case: {case['note']}. Got: '{login.error_text()}'"
        )
