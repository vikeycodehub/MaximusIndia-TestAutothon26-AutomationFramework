"""Non-intrusive, standalone self-healing wrappers for Playwright actions.

These helpers are plain functions - not mixins or base-class overrides - so
existing page objects and tests can adopt them incrementally by simply
importing `smart_click` / `smart_fill` instead of calling `page.click()` /
`page.fill()` directly. Nothing here modifies `base_page.py` or any existing
class.

Enable/disable via the ENABLE_AI_HEALING environment variable (default: off).
"""
from __future__ import annotations

import os

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from framework.ai.llm_client import get_client
from framework.core.logger import get_logger

logger = get_logger("ai.self_healing")


def _ai_healing_enabled() -> bool:
    return os.getenv("ENABLE_AI_HEALING", "false").strip().lower() == "true"


def _heal_selector(page: Page, description: str) -> str | None:
    """Best-effort attempt to get an AI-suggested selector; never raises."""
    try:
        page_source = page.content()
    except Exception:  # noqa: BLE001 - page may already be in a bad state
        logger.exception("Could not capture page.content() for self-healing.")
        return None

    try:
        return get_client().heal_locator(description, page_source)
    except Exception:  # noqa: BLE001 - AI errors must never crash the test
        logger.exception("AI heal_locator() call failed.")
        return None


def smart_click(page: Page, primary_selector: str, description: str, timeout: float | None = None) -> None:
    """Click `primary_selector`; on timeout, fall back to an AI-healed selector.

    Raises the original Playwright TimeoutError if AI healing is disabled,
    unavailable, or also fails - callers keep their normal failure behavior.
    """
    try:
        kwargs = {"timeout": timeout} if timeout is not None else {}
        page.click(primary_selector, **kwargs)
        logger.info("smart_click: standard click succeeded for selector '%s'.", primary_selector)
        return
    except PlaywrightTimeoutError as exc:
        if not _ai_healing_enabled():
            raise

        logger.warning(
            "smart_click: standard click timed out for '%s'; attempting AI self-healing.",
            primary_selector,
        )
        healed_selector = _heal_selector(page, description)
        if not healed_selector:
            logger.warning("smart_click: AI healing produced no selector; re-raising original error.")
            raise

        try:
            page.click(healed_selector)
            logger.info(
                "smart_click: AI self-healed execution succeeded using selector '%s'.",
                healed_selector,
            )
        except Exception:
            logger.exception(
                "smart_click: AI-suggested selector '%s' also failed; re-raising original error.",
                healed_selector,
            )
            raise exc


def smart_fill(
    page: Page,
    primary_selector: str,
    value: str,
    description: str,
    timeout: float | None = None,
) -> None:
    """Fill `primary_selector` with `value`; on timeout, fall back to an AI-healed selector.

    Raises the original Playwright TimeoutError if AI healing is disabled,
    unavailable, or also fails - callers keep their normal failure behavior.
    """
    try:
        kwargs = {"timeout": timeout} if timeout is not None else {}
        page.fill(primary_selector, value, **kwargs)
        logger.info("smart_fill: standard fill succeeded for selector '%s'.", primary_selector)
        return
    except PlaywrightTimeoutError as exc:
        if not _ai_healing_enabled():
            raise

        logger.warning(
            "smart_fill: standard fill timed out for '%s'; attempting AI self-healing.",
            primary_selector,
        )
        healed_selector = _heal_selector(page, description)
        if not healed_selector:
            logger.warning("smart_fill: AI healing produced no selector; re-raising original error.")
            raise

        try:
            page.fill(healed_selector, value)
            logger.info(
                "smart_fill: AI self-healed execution succeeded using selector '%s'.",
                healed_selector,
            )
        except Exception:
            logger.exception(
                "smart_fill: AI-suggested selector '%s' also failed; re-raising original error.",
                healed_selector,
            )
            raise exc
