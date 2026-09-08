"""
Thin API client wrapper - useful for:
- test data setup/teardown via API (faster than UI)
- Bug Quest backend validation (compare UI state vs API truth)
"""
from __future__ import annotations

from typing import Any

import requests

from framework.config.settings import settings
from framework.core.logger import get_logger

logger = get_logger(__name__)


class ApiClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.api_base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _url(self, path: str) -> str:
        return path if path.startswith("http") else f"{self.base_url}{path}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        logger.info("GET %s", url)
        return self.session.get(url, timeout=15, **kwargs)

    def post(self, path: str, json: dict | None = None, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        logger.info("POST %s payload=%s", url, json)
        return self.session.post(url, json=json, timeout=15, **kwargs)

    def put(self, path: str, json: dict | None = None, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        logger.info("PUT %s payload=%s", url, json)
        return self.session.put(url, json=json, timeout=15, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        logger.info("DELETE %s", url)
        return self.session.delete(url, timeout=15, **kwargs)
