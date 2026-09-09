"""Optional AI-powered failure enrichment for Pytest, decoupled from conftest.py.

This module is NOT auto-loaded as a plugin. To use it, import the helper
function from your existing `conftest.py` hooks (see usage below) - nothing
here changes if you never import it.

Usage (inside the existing conftest.py `pytest_runtest_makereport` hook):

    from framework.ai.ai_reporter import attach_ai_rca

    if rep.when == "call" and rep.failed:
        attach_ai_rca(item, rep, page=item.funcargs.get("page"))

Enable/disable via the ENABLE_AI_RCA environment variable (default: off).
Every operation is wrapped in try/except so this can never fail a test run.
"""
from __future__ import annotations

import os

from framework.ai.llm_client import get_client
from framework.core.logger import get_logger

logger = get_logger("ai.reporter")


def _ai_rca_enabled() -> bool:
    return os.getenv("ENABLE_AI_RCA", "false").strip().lower() == "true"


def analyze_and_store(item, error_trace: str, page_source: str = "") -> str | None:
    """Run AI root-cause analysis and store the result on `item`; returns the summary.

    The summary is stashed at `item._ai_rca` (and inside pytest's `item.stash`/
    `_store` mechanism when available) so other fixtures/plugins can read it.
    Never raises - any failure is logged and results in None.
    """
    if not _ai_rca_enabled():
        return None

    try:
        summary = get_client().analyze_failure(error_trace or "", page_source or "")
    except Exception:  # noqa: BLE001 - AI errors must never crash the test run
        logger.exception("AI RCA analysis failed.")
        return None

    if not summary:
        return None

    try:
        setattr(item, "_ai_rca", summary)
        store = getattr(item, "_store", None)
        if store is not None:
            store["ai_rca"] = summary
    except Exception:  # noqa: BLE001 - storage is best-effort only
        logger.exception("Could not attach AI RCA summary to test item.")

    logger.info("AI RCA summary for '%s': %s", getattr(item, "name", "<unknown>"), summary)
    return summary


def attach_ai_rca(item, rep, page=None) -> str | None:
    """Convenience wrapper: build inputs from a failed pytest report and analyze.

    `rep` is the TestReport passed to pytest_runtest_makereport (must have
    `.longreprtext`). `page` is an optional Playwright Page used to capture
    the current HTML for extra context.
    """
    if not _ai_rca_enabled():
        return None

    try:
        error_trace = getattr(rep, "longreprtext", "") or str(getattr(rep, "longrepr", ""))
    except Exception:  # noqa: BLE001
        error_trace = ""

    page_source = ""
    if page is not None:
        try:
            page_source = page.content()
        except Exception:  # noqa: BLE001 - page may be closed/broken after failure
            logger.exception("Could not capture page.content() for AI RCA.")

    return analyze_and_store(item, error_trace, page_source)


def print_ai_rca_to_terminal(terminalreporter, item_name: str, summary: str) -> None:
    """Best-effort helper to echo the AI RCA summary to the Pytest terminal output."""
    try:
        terminalreporter.write_sep("-", f"AI Root-Cause Analysis: {item_name}")
        terminalreporter.write_line(summary)
    except Exception:  # noqa: BLE001 - terminal output is never critical
        logger.exception("Could not write AI RCA summary to terminal.")
