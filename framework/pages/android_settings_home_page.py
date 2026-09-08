"""
Sample native Android Page Object using the pre-installed Settings app - safe to
run on any emulator/device with zero setup (no APK needed). Proves the Appium
wiring end to end. Tomorrow: replace with page objects for the real AUT once the
APK / package name / activity are known (set ANDROID_APP_PACKAGE, ANDROID_APP_ACTIVITY,
ANDROID_APP_PATH in .env).
"""
from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from framework.core.base_mobile_page import BaseMobilePage


class AndroidSettingsHomePage(BaseMobilePage):
    SEARCH_ICON = (AppiumBy.ID, "com.android.settings:id/search_action_bar")
    TITLE = (AppiumBy.ID, "com.android.settings:id/homepage_title")

    def title_text(self) -> str:
        return self.text_of(*self.TITLE)

    def is_loaded(self) -> bool:
        return self.is_present(*self.TITLE)
