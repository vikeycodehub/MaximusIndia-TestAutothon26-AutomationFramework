"""
Login / OTP screen of Gajab (India's Bargain Bazaar) - https://stg.gajab.com/

Selectors verified live against the staging site on 2026-09-09 (mobile-number
signin -> 6-digit OTP -> submit). The site renders duplicate desktop/mobile
DOM nodes sharing the same id for some header controls, so we always target
`.first()` to avoid Playwright strict-mode violations.
"""
from __future__ import annotations

from framework.config.settings import settings
from framework.core.base_page import BasePage

BASE_URL = settings.base_url
DEFAULT_OTP = "123456"


class GajabLoginPage(BasePage):
    LOGIN_LINK = "a[href='/auth/signin']"
    MOBILE_INPUT = "#signin-mobile-input"
    TERMS_CHECKBOX = "#signin-terms-checkbox"
    REQUEST_OTP_BTN = "#signin-submit-btn"
    OTP_INPUT = "#otp-input-{index}"
    OTP_SUBMIT_BTN = "#otp-submit-btn"

    def open(self) -> "GajabLoginPage":
        self.goto(BASE_URL)
        return self

    def go_to_signin(self) -> "GajabLoginPage":
        # force=True: staging header keeps animating (rotating banner/placeholder text),
        # so Playwright's "stable" actionability check never settles.
        self.page.locator(self.LOGIN_LINK).first.click(timeout=self.timeout, force=True)
        return self

    def request_otp(self, mobile_number: str) -> "GajabLoginPage":
        self.page.locator(self.MOBILE_INPUT).fill(mobile_number, timeout=self.timeout)
        # Both controls are covered by an animated overlay layer, so coordinate-based
        # clicks (even force=True) land on the wrong element; dispatching a raw DOM
        # 'click' targets the exact node and reliably triggers React's handler.
        self.page.locator(self.TERMS_CHECKBOX).dispatch_event("click")
        self.page.locator(self.REQUEST_OTP_BTN).dispatch_event("click")
        return self

    def enter_otp(self, otp: str = DEFAULT_OTP) -> "GajabLoginPage":
        for index, digit in enumerate(otp):
            locator = self.page.locator(self.OTP_INPUT.format(index=index))
            # force=True: same overlay/stability issue as the header controls above.
            locator.click(timeout=self.timeout, force=True)
            self.page.keyboard.type(digit, delay=80)
        return self

    def submit_otp(self) -> "GajabLoginPage":
        self.page.locator(self.OTP_SUBMIT_BTN).dispatch_event("click")
        return self

    def login_with_mobile(self, mobile_number: str, otp: str = DEFAULT_OTP) -> None:
        self.go_to_signin()
        self.request_otp(mobile_number)
        self.enter_otp(otp)
        self.submit_otp()

    def is_logged_in(self) -> bool:
        """After a successful login the 'Log in / Sign up' link disappears from the header."""
        self.page.wait_for_timeout(1000)
        return self.page.locator(self.LOGIN_LINK).count() == 0
