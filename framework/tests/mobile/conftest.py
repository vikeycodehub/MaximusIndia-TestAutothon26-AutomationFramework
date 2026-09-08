"""
Fixture for native Android (Appium) tests. Lives here (not root conftest.py) so
importing `appium` is only required when these tests actually run.
"""
from __future__ import annotations

import pytest

from framework.core.appium_driver import appium_server_reachable, build_android_driver


@pytest.fixture
def appium_driver():
    if not appium_server_reachable():
        pytest.skip(
            "Appium server not reachable - start it with scripts/start_appium_server.ps1 "
            "and ensure a device/emulator is connected."
        )
    driver = build_android_driver()
    yield driver
    driver.quit()
