"""
End-to-end critical business flow: login -> add product to cart -> checkout ->
order confirmation. This is the single most important test in the suite -
it's the "does the core revenue flow work" check to run before every demo.
"""
import allure
import pytest

from framework.pages.saucedemo.cart_page import CartPage
from framework.pages.saucedemo.checkout_pages import (
    CheckoutCompletePage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
)
from framework.pages.saucedemo.inventory_page import InventoryPage
from framework.pages.saucedemo.login_page import LoginPage


@allure.feature("SauceDemo - Checkout")
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.web
def test_end_to_end_purchase_flow(page):
    # 1. Login
    login = LoginPage(page).open()
    login.login("standard_user", "secret_sauce")

    # 2. Add a product to the cart and go to cart
    inventory = InventoryPage(page)
    inventory.add_to_cart_by_product_id("sauce-labs-backpack")
    assert inventory.cart_count() == 1, "Cart badge should show 1 item"
    inventory.go_to_cart()

    # 3. Verify cart contents, proceed to checkout
    cart = CartPage(page)
    assert "Sauce Labs Backpack" in cart.item_names()
    cart.checkout()

    # 4. Fill shipping info
    step_one = CheckoutStepOnePage(page)
    step_one.fill_info("John", "Doe", "12345")
    step_one.continue_to_overview()

    # 5. Verify order summary total, finish order
    step_two = CheckoutStepTwoPage(page)
    assert "Total:" in step_two.total_text()
    step_two.finish()

    # 6. Verify order confirmation
    complete = CheckoutCompletePage(page)
    assert complete.is_order_complete()
    assert "Thank you for your order" in complete.header_text()


@allure.feature("SauceDemo - Checkout")
@pytest.mark.regression
@pytest.mark.web
def test_checkout_requires_shipping_info(page):
    """Negative test: continuing without required fields should show a validation error."""
    login = LoginPage(page).open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_to_cart_by_product_id("sauce-labs-backpack")
    inventory.go_to_cart()

    cart = CartPage(page)
    cart.checkout()

    step_one = CheckoutStepOnePage(page)
    step_one.continue_to_overview()  # leave all fields empty

    assert step_one.has_error(), "Should show a validation error when required fields are empty"
