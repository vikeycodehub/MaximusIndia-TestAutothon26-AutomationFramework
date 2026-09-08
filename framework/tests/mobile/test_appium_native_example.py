"""
Native Android app automation example via Appium (UiAutomator2 driver).
Skips gracefully if no Appium server is running - safe to keep in the suite.

This is the track to use tomorrow if the challenge app is a genuine native
Android app (not web/hybrid/WebView, which the Playwright Android track handles).
"""
import allure
import pytest

from framework.pages.android_settings_home_page import AndroidSettingsHomePage


@allure.feature("Native Android - Smoke")
@pytest.mark.smoke
@pytest.mark.appium
def test_settings_app_home_loads(appium_driver):
    home = AndroidSettingsHomePage(appium_driver)
    assert home.is_loaded(), "Settings app home screen should be visible"
