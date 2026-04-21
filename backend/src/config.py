import os
import json
from dotenv import load_dotenv

load_dotenv()

# ─── Multi-key support ────────────────────────────────────────────────────────
# Option A: single key via GITHUB_TOKEN (legacy, treated as "Default")
# Option B: JSON map via GITHUB_TOKENS_JSON, e.g.:
#   GITHUB_TOKENS_JSON='{"Alice": "ghp_xxx", "Bob": "ghp_yyy"}'

_raw_json = os.getenv("GITHUB_TOKENS_JSON", "")
_single   = os.getenv("GITHUB_TOKEN", "")

if _raw_json:
    try:
        API_KEYS: dict[str, str] = json.loads(_raw_json)
    except json.JSONDecodeError:
        print("[config] WARNING: GITHUB_TOKENS_JSON is not valid JSON — ignoring.")
        API_KEYS = {}
elif _single:
    API_KEYS = {"Default": _single}
else:
    API_KEYS = {}

_active_key: str = next(iter(API_KEYS), "") if API_KEYS else ""


def get_active_key_name() -> str:
    return _active_key


def set_active_key(name: str) -> bool:
    global _active_key
    if name in API_KEYS:
        _active_key = name
        return True
    return False


def get_headers() -> dict:
    """Always returns headers for the currently-active key. Call this per-request."""
    token = API_KEYS.get(_active_key, "")
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


# Legacy alias — modules that import HEADERS directly will get a dict that
# points to the same object. Use get_headers() for fresh headers per request.
HEADERS = get_headers()

# Startup log
if API_KEYS:
    names = ", ".join(API_KEYS.keys())
    print(f"[config] {len(API_KEYS)} API key(s) loaded: {names}")
    print(f"[config] Active key: '{_active_key}' — authenticated (5000 req/hr)")
else:
    print("[config] WARNING: No GitHub token set — unauthenticated (60 req/hr limit)")
