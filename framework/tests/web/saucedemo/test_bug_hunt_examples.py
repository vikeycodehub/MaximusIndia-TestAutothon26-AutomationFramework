"""
Bug Quest demo: SauceDemo seeds intentional bugs behind special usernames.
This file shows how to turn manual "exploratory" findings into automated
regression checks with clear evidence - exactly what judges want to see for
Bug Quest: a reproducible, evidence-backed defect, not just a text report.

Known seeded bug (verified manually before writing this test):
  BUG-001: logging in as `problem_user` shows the IDENTICAL broken image
  (sl-404.jpg) for every product on the Products page, instead of each
  product's real image.

We assert the CORRECT behavior (unique images per product). Today this test
is expected to FAIL for problem_user (marked xfail so the suite stays green
while still proving the bug is caught) - if SauceDemo ever fixes it, xfail's
strict mode will flag the XPASS so we notice immediately.
"""
import allure
import pytest

from framework.pages.saucedemo.inventory_page import InventoryPage
from framework.pages.saucedemo.login_page import LoginPage


@allure.feature("SauceDemo - Bug Quest")
@pytest.mark.regression
@pytest.mark.web
@pytest.mark.xfail(
    reason="BUG-001: problem_user shows identical broken image for every product",
    strict=True,
)
def test_problem_user_product_images_should_be_unique(page):
    login = LoginPage(page).open()
    login.login("problem_user", "secret_sauce")

    inventory = InventoryPage(page)
    image_sources = inventory.item_image_sources()

    assert len(set(image_sources)) > 1, (
        f"All product images are identical ({image_sources[0]}) - broken image bug reproduced"
    )


@allure.feature("SauceDemo - Bug Quest")
@pytest.mark.smoke
@pytest.mark.web
def test_locked_out_user_is_blocked_with_clear_message(page):
    """Not a bug - confirms the locked-out safeguard works and shows a clear message."""
    login = LoginPage(page).open()
    login.login("locked_out_user", "secret_sauce")

    assert login.has_error()
    assert "locked out" in login.error_text().lower()
