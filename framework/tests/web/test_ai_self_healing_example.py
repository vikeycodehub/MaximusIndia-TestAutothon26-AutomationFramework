"""Standalone example proving framework/ai/self_healing.py works end-to-end.

This test does NOT touch LoginPage/BasePage - it drives the page directly
with smart_click/smart_fill to demonstrate AI self-healing kicking in when a
selector is stale. Requires ENABLE_AI_HEALING=true and a valid AI provider
key in .env; otherwise the intentionally-wrong selector will simply raise the
normal Playwright TimeoutError (no different from vanilla Playwright).
"""
from framework.ai.self_healing import smart_click, smart_fill

BASE_URL = "https://www.saucedemo.com/"


def test_ai_self_healing_login(page):
    page.goto(BASE_URL)

    # Correct selector - standard Playwright path, no AI involved.
    smart_fill(page, "#user-name", "standard_user", "the username input field", timeout=5000)

    # Deliberately wrong selector to force the AI self-healing fallback.
    smart_fill(
        page,
        "#password-wrong-selector",
        "secret_sauce",
        "the password input field",
        timeout=5000,
    )

    smart_click(page, "#login-button", "the green Login submit button", timeout=5000)

    assert "inventory.html" in page.url
