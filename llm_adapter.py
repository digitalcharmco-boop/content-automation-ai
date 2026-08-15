"""
Lightweight LLM adapter supporting Gemini or Grok (and a generic HTTP endpoint).

Usage:
  - Set LLM_PROVIDER to "gemini" or "grok" (or use PROVIDER_URL to point to any HTTP endpoint).
  - Set provider-specific API key env var(s):
      - For Gemini: GEMINI_API_KEY (or PROVIDER_API_KEY)
      - For Grok: GROK_API_KEY (or PROVIDER_API_KEY)
  - Optionally set PROVIDER_URL to an explicit endpoint if you don't want to rely on built-in defaults.
This adapter intentionally uses simple HTTP POSTs and flexible response parsing.
For production use, use the official SDKs (Google client libs for Gemini; xAI SDK for Grok).
"""
from typing import Optional
import os
import requests
import json

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").strip().lower()
PROVIDER_URL = os.getenv("PROVIDER_URL")         # optional explicit endpoint override
API_KEY = os.getenv("PROVIDER_API_KEY")         # generic key name
TIMEOUT = int(os.getenv("PROVIDER_TIMEOUT", "60"))
MODEL = os.getenv("PROVIDER_MODEL", "").strip()  # provider model name if needed

# Provider-specific env aliases
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")


def _normalize_text_from_json(data: dict) -> Optional[str]:
    """Try common response shapes and return a text string if found."""
    if not isinstance(data, dict):
        return None

    # Common shapes:
    # - Google Gemini (Generative API): {"candidates": [{"content": "..."}, ...]} or {"candidates":[{"output":"..."}]}
    if "candidates" in data and isinstance(data["candidates"], list) and data["candidates"]:
        first = data["candidates"][0]
        # content, output, or text
        return first.get("content") or first.get("output") or first.get("text")

    # - OpenAI-like: {"choices":[{"text": "..."}]}
    if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
        choice = data["choices"][0]
        return choice.get("text") or (choice.get("message") and choice["message"].get("content"))

    # - Grok or other: {"outputs":[{"content":"..."}]} or {"output_text": "..."} or {"text":"..."}
    if "outputs" in data and isinstance(data["outputs"], list) and data["outputs"]:
        o = data["outputs"][0]
        if isinstance(o, dict):
            return o.get("content") or o.get("text")
    if "output_text" in data:
        return data["output_text"]
    if "text" in data:
        return data["text"]
    if "result" in data and isinstance(data["result"], str):
        return data["result"]

    # Fallbacks: see if there's any top-level stringy value
    for k, v in data.items():
        if isinstance(v, str) and len(v) > 20:
            return v

    return None


def call_generic_http(prompt: str, url: str, key: str, model: Optional[str] = None) -> str:
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"input": prompt}
    if model:
        payload["model"] = model

    r = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    try:
        data = r.json()
    except Exception:
        return r.text
    text = _normalize_text_from_json(data)
    return text if text is not None else json.dumps(data)


def call_gemini(prompt: str) -> str:
    """
    Gemini (Google) helper.
    NOTE: prefer Google client libraries for production (service accounts / OAuth).
    This helper expects either:
      - PROVIDER_URL set to a valid Gemini REST endpoint (e.g., Google's generate endpoint),
      - or GEMINI_API_KEY set plus PROVIDER_URL set.
    If you don't set PROVIDER_URL, you must provide a valid endpoint in env.
    """
    key = API_KEY or GEMINI_API_KEY
    url = PROVIDER_URL
    if not key:
        raise RuntimeError("Gemini API key not set (GEMINI_API_KEY or PROVIDER_API_KEY)")
    if not url:
        raise RuntimeError("Please set PROVIDER_URL to the Gemini REST endpoint (see README).")
    return call_generic_http(prompt, url, key, model=MODEL or None)


def call_grok(prompt: str) -> str:
    """
    Grok (xAI) helper.
    NOTE: xAI may provide SDKs — use official SDK if available. This helper expects:
      - GROK_API_KEY or PROVIDER_API_KEY
      - PROVIDER_URL set to the grok endpoint (if needed)
    """
    key = API_KEY or GROK_API_KEY
    url = PROVIDER_URL
    if not key:
        raise RuntimeError("Grok API key not set (GROK_API_KEY or PROVIDER_API_KEY)")
    if not url:
        raise RuntimeError("Please set PROVIDER_URL to the Grok REST endpoint (see provider docs).")
    return call_generic_http(prompt, url, key, model=MODEL or None)


def generate(prompt: str) -> str:
    provider = LLM_PROVIDER or os.getenv("PROVIDER", "").strip().lower()
    if provider in ("gemini", "google", "google_gemini"):
        return call_gemini(prompt)
    if provider in ("grok", "xai"):
        return call_grok(prompt)
    # Fallback: if PROVIDER_URL + PROVIDER_API_KEY set, call generic
    if PROVIDER_URL and (API_KEY or GEMINI_API_KEY or GROK_API_KEY):
        key = API_KEY or GEMINI_API_KEY or GROK_API_KEY
        return call_generic_http(prompt, PROVIDER_URL, key, model=MODEL or None)

    raise RuntimeError(
        "No LLM provider configured. Set LLM_PROVIDER (gemini|grok) and provider-specific API key, "
        "or set PROVIDER_URL and PROVIDER_API_KEY."
    )


if __name__ == "__main__":
    # Quick local test (needs PROVIDER_URL + PROVIDER_API_KEY or provider-specific envs)
    try:
        print(generate("Say hello and describe your name and purpose in one short sentence."))
    except Exception as e:
        print("ERROR:", str(e))
        raise
