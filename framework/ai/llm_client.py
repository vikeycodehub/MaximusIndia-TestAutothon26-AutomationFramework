"""Thin wrapper around the OpenAI SDK that transparently supports either
OpenAI (GPT-4o / GPT-4o-mini) or DeepSeek (deepseek-chat) as the backing LLM.

Provider selection is driven entirely by environment variables so this module
can be dropped into any project without touching existing code:

    AI_PROVIDER        "openai" (default) or "deepseek"
    OPENAI_API_KEY      required when AI_PROVIDER=openai
    OPENAI_MODEL        optional, defaults to "gpt-4o-mini"
    DEEPSEEK_API_KEY    required when AI_PROVIDER=deepseek
    DEEPSEEK_MODEL      optional, defaults to "deepseek-chat"

Every public method is wrapped in try/except so a network error, missing key,
or malformed response never raises out of this module - callers always get a
best-effort string back (or None) instead of an exception.
"""
from __future__ import annotations

import os

from framework.core.logger import get_logger

logger = get_logger("ai.llm_client")

_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
_DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
_DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"


class LLMClient:
    """Provider-agnostic chat-completion client for OpenAI or DeepSeek."""

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai").strip().lower()
        self.model = self._resolve_model()
        self._client = self._build_client()

    def _resolve_model(self) -> str:
        if self.provider == "deepseek":
            return os.getenv("DEEPSEEK_MODEL", _DEFAULT_DEEPSEEK_MODEL)
        return os.getenv("OPENAI_MODEL", _DEFAULT_OPENAI_MODEL)

    def _build_client(self):
        try:
            from openai import OpenAI
        except ImportError:
            logger.warning("openai package not installed; AI features are disabled.")
            return None

        try:
            if self.provider == "deepseek":
                api_key = os.getenv("DEEPSEEK_API_KEY")
                if not api_key:
                    logger.warning("DEEPSEEK_API_KEY not set; AI features are disabled.")
                    return None
                return OpenAI(api_key=api_key, base_url=_DEEPSEEK_BASE_URL)

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OPENAI_API_KEY not set; AI features are disabled.")
                return None
            return OpenAI(api_key=api_key)
        except Exception:  # noqa: BLE001 - client construction must never crash tests
            logger.exception("Failed to initialize LLM client for provider '%s'.", self.provider)
            return None

    def _chat(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str | None:
        """Send a single-turn chat completion request; returns None on any failure."""
        if self._client is None:
            return None

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception:  # noqa: BLE001 - never let an API/network error bubble up
            logger.exception("LLM request failed (provider=%s, model=%s).", self.provider, self.model)
            return None

    def heal_locator(self, target_description: str, page_source: str) -> str | None:
        """Ask the LLM to suggest a corrected CSS/XPath selector for the given element.

        Returns a single selector string (no explanation), or None on failure.
        """
        system_prompt = (
            "You are a Playwright test automation expert. Given a description of a "
            "target UI element and the current page HTML, respond with ONLY a single "
            "working CSS or XPath selector that best matches the element. Do not "
            "include explanations, markdown, or code fences - output the raw selector "
            "string only."
        )
        truncated_source = (page_source or "")[:12000]
        user_prompt = (
            f"Target element description: {target_description}\n\n"
            f"Page HTML (truncated):\n{truncated_source}"
        )
        selector = self._chat(system_prompt, user_prompt, max_tokens=200)
        if not selector:
            return None
        return selector.strip().strip("`").strip()

    def analyze_failure(self, error_trace: str, page_source: str) -> str | None:
        """Ask the LLM for a concise 2-sentence root-cause summary of a test failure."""
        system_prompt = (
            "You are a senior QA automation engineer performing root-cause analysis "
            "on a failed Playwright/Pytest test. Respond with EXACTLY two sentences: "
            "the first stating the most likely root cause, the second suggesting a "
            "fix or next diagnostic step. Be concise and specific."
        )
        truncated_source = (page_source or "")[:8000]
        user_prompt = (
            f"Error trace:\n{error_trace}\n\n"
            f"Page HTML at time of failure (truncated):\n{truncated_source}"
        )
        return self._chat(system_prompt, user_prompt, max_tokens=250)

    def generate_bug_report(self, error_log: str, screenshot_path: str | None) -> str | None:
        """Ask the LLM to draft a formatted markdown bug report for the given failure."""
        system_prompt = (
            "You are a QA engineer writing a bug report. Given an error log and the "
            "path to a failure screenshot, produce a concise markdown bug report with "
            "these sections: '## Summary', '## Steps to Reproduce', '## Expected "
            "Result', '## Actual Result', and '## Attachments'. Reference the "
            "screenshot path under Attachments. Keep it short and readable."
        )
        user_prompt = (
            f"Error log:\n{error_log}\n\n"
            f"Screenshot path: {screenshot_path or 'N/A'}"
        )
        return self._chat(system_prompt, user_prompt, max_tokens=600)


_default_client: LLMClient | None = None


def get_client() -> LLMClient:
    """Lazily construct and cache a module-level LLMClient instance."""
    global _default_client
    if _default_client is None:
        _default_client = LLMClient()
    return _default_client
