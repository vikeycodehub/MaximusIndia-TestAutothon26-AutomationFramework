"""Flow 01: staging navigation, mobile login, OTP, and login verification."""
from __future__ import annotations

import random

import pytest

from framework.pages.gajab.login_page import GajabLoginPage


@pytest.mark.web
@pytest.mark.critical
def test_login_with_default_otp(page):
    mobile_number = "9" + "".join(str(random.randint(0, 9)) for _ in range(9))
    login_page = GajabLoginPage(page).open()

    login_page.login_with_mobile(mobile_number)

    assert login_page.is_logged_in(), "The login/sign-up control should disappear after OTP verification"
