"""
Root pytest configuration.

Provides:
- CLI option --env to switch environments on the fly
- browser_context_args override (base_url, viewport, video/trace capture)
- automatic screenshot + trace attachment to Allure on failure
- a `settings` fixture for tests/pages that need config
"""
from __future__ import annotations

import os
from pathlib import Path

import allure
import pytest

from framework.config.settings import settings as app_settings
from framework.ai.ai_reporter import attach_ai_rca

REPORTS_DIR = Path(__file__).parent / "reports"
TRACE_DIR = REPORTS_DIR / "traces"
VIDEO_DIR = REPORTS_DIR / "videos"
SCREENSHOT_DIR = REPORTS_DIR / "screenshots"
for d in (TRACE_DIR, VIDEO_DIR, SCREENSHOT_DIR):
    d.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Override TEST_ENV (dev/qa/stage) for this run.",
    )


def pytest_configure(config):
    env_override = config.getoption("--env")
    if env_override:
        os.environ["TEST_ENV"] = env_override


@pytest.fixture(scope="session")
def settings():
    return app_settings


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Extend pytest-playwright's default context args with our config."""
    return {
        **browser_context_args,
        "base_url": app_settings.base_url,
        "viewport": {"width": 1440, "height": 900},
        "record_video_dir": str(VIDEO_DIR),
        "ignore_https_errors": True,
    }


@pytest.fixture(autouse=True)
def _tracing(context, request):
    """Start/stop Playwright tracing per test; only saved when the test fails."""
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    trace_path = TRACE_DIR / f"{request.node.name}.zip"
    context.tracing.stop(path=str(trace_path))
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        allure.attach.file(
            str(trace_path), name="trace", attachment_type="application/zip", extension="zip"
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose test result on the item so fixtures can check pass/fail, and
    auto-attach a screenshot + page HTML to Allure on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page is not None:
            try:
                screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(
                    str(screenshot_path),
                    name="failure-screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    page.content(), name="page-html", attachment_type=allure.attachment_type.HTML
                )
            except Exception:  # noqa: BLE001 - never fail the test because of reporting
                pass

        summary = attach_ai_rca(item, rep, page=page)
        if summary:
            try:
                allure.attach(summary, name="ai-root-cause-analysis", attachment_type=allure.attachment_type.TEXT)
            except Exception:  # noqa: BLE001 - never fail the test because of reporting
                pass
