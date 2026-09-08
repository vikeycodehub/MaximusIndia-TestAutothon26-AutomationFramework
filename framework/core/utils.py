"""Small shared helpers used across tests: data loading and retry logic."""
from __future__ import annotations

import functools
import json
import time
from pathlib import Path
from typing import Any, Callable, TypeVar

from framework.core.logger import get_logger

logger = get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

T = TypeVar("T")


def load_json_data(filename: str) -> Any:
    """Load a JSON fixture from framework/data/<filename>."""
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def retry(times: int = 3, delay_seconds: float = 1.0, exceptions: tuple = (Exception,)):
    """Retry decorator for flaky steps (e.g. network hiccups in API calls)."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # noqa: PERF203
                    last_exc = exc
                    logger.warning(
                        "Attempt %s/%s failed for %s: %s", attempt, times, func.__name__, exc
                    )
                    if attempt < times:
                        time.sleep(delay_seconds)
            raise last_exc  # type: ignore[misc]

        return wrapper

    return decorator
