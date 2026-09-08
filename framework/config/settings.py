"""
Central configuration loader for the framework.

Tomorrow, when the real Application Under Test (AUT) is announced:
1. Update framework/config/environments.json with the real base_url / api_base_url.
2. Or simply export TEST_ENV / override via .env - no code changes needed.
"""
import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = Path(__file__).parent
ENVIRONMENTS_FILE = CONFIG_DIR / "environments.json"


@dataclass
class Settings:
    env: str
    base_url: str
    api_base_url: str
    headless: bool
    browser: str
    default_timeout_ms: int
    # Appium / native Android
    appium_server_url: str
    android_app_package: str
    android_app_activity: str
    android_app_path: str
    android_device_name: str
    android_platform_version: str


def _str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def load_settings() -> Settings:
    env = os.getenv("TEST_ENV", "dev").lower()

    with open(ENVIRONMENTS_FILE, "r", encoding="utf-8") as f:
        environments = json.load(f)

    if env not in environments:
        raise ValueError(
            f"Unknown TEST_ENV='{env}'. Valid options: {list(environments.keys())}. "
            f"Add it to {ENVIRONMENTS_FILE} if it's a new environment."
        )

    env_cfg = environments[env]

    return Settings(
        env=env,
        base_url=os.getenv("BASE_URL", env_cfg["base_url"]),
        api_base_url=os.getenv("API_BASE_URL", env_cfg["api_base_url"]),
        headless=_str_to_bool(os.getenv("HEADLESS", "true")),
        browser=os.getenv("BROWSER", "chromium"),
        default_timeout_ms=int(os.getenv("DEFAULT_TIMEOUT_MS", "15000")),
        appium_server_url=os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723"),
        android_app_package=os.getenv("ANDROID_APP_PACKAGE", "com.android.settings"),
        android_app_activity=os.getenv("ANDROID_APP_ACTIVITY", ".Settings"),
        android_app_path=os.getenv("ANDROID_APP_PATH", ""),
        android_device_name=os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
        android_platform_version=os.getenv("ANDROID_PLATFORM_VERSION", ""),
    )


settings = load_settings()
