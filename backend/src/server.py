from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import httpx

from analyzer import analyze_repo
from config import API_KEYS, get_active_key_name, set_active_key, get_headers


app = FastAPI()

# ---------------------------------------------------------------------------
# Simple in-memory TTL cache
# ---------------------------------------------------------------------------
_cache: dict = {}
ANALYZE_TTL = int(os.getenv("ANALYZE_CACHE_TTL", 3600))   # 1 hour default
REPOS_TTL   = int(os.getenv("REPOS_CACHE_TTL",   300))    # 5 minutes default

def _cache_get(key: str):
    entry = _cache.get(key)
    if entry and time.time() < entry["expires_at"]:
        return entry["data"]
    return None

def _cache_set(key: str, data, ttl: int):
    _cache[key] = {"data": data, "expires_at": time.time() + ttl}
# ---------------------------------------------------------------------------

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepoRequest(BaseModel):
    owner: str
    repo: str
    threshold: int
    days: int = 90


@app.get("/repos/{owner}")
async def list_repos(owner: str):
    """Return repos for an owner (user or org), sorted by most recently updated."""
    cache_key = f"repos:{owner}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    async with httpx.AsyncClient() as client:
        # Try user endpoint first, fall back to org
        for kind in ("users", "orgs"):
            response = await client.get(
                f"https://api.github.com/{kind}/{owner}/repos",
                headers=get_headers(),
                params={"per_page": 100, "sort": "updated", "direction": "desc"},
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                result = [
                    {
                        "name": r["name"],
                        "description": r.get("description") or "",
                        "stars": r["stargazers_count"],
                        "language": r.get("language") or "",
                        "private": r["private"],
                    }
                    for r in data
                    if not r["private"]
                ]
                _cache_set(cache_key, result, REPOS_TTL)
                return result

    raise HTTPException(status_code=404, detail=f"Owner '{owner}' not found on GitHub.")


@app.post("/analyze")
async def analyze(data: RepoRequest):
    cache_key = f"analyze:{data.owner}:{data.repo}:{data.threshold}:{data.days}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    # Pre-flight: verify repo exists before running full analysis
    async with httpx.AsyncClient() as client:
        check = await client.get(
            f"https://api.github.com/repos/{data.owner}/{data.repo}",
            headers=get_headers(),
            timeout=10,
        )

    if check.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Repository '{data.owner}/{data.repo}' not found. Check the owner and repo name.",
        )
    if check.status_code == 403:
        raise HTTPException(status_code=403, detail="GitHub API rate limit exceeded. Try again later.")
    if check.status_code != 200:
        raise HTTPException(status_code=502, detail="GitHub API returned an unexpected error.")

    repo_meta = check.json()

    start = time.time()
    result = await analyze_repo(
        data.owner,
        data.repo,
        data.threshold,
        data.days,
    )
    print("Total Time:", time.time() - start)

    # Attach repo metadata to the response
    result["Repo Meta"] = {
        "full_name": repo_meta["full_name"],
        "description": repo_meta.get("description") or "",
        "stars": repo_meta["stargazers_count"],
        "forks": repo_meta["forks_count"],
        "open_issues": repo_meta["open_issues_count"],
        "language": repo_meta.get("language") or "Unknown",
        "url": repo_meta["html_url"],
    }

    _cache_set(cache_key, result, ANALYZE_TTL)
    return result


@app.delete("/cache")
async def clear_cache():
    """Manually bust the entire cache (useful during development)."""
    _cache.clear()
    return {"message": "Cache cleared."}


# ─── API Key Management ───────────────────────────────────────────────────────

@app.get("/keys")
async def list_keys():
    """Return available key names and which one is active. Never exposes token values."""
    return {
        "keys": list(API_KEYS.keys()),
        "active": get_active_key_name(),
        "authenticated": bool(API_KEYS),
    }


class SwitchKeyRequest(BaseModel):
    name: str


@app.post("/keys/active")
async def switch_key(body: SwitchKeyRequest):
    """Switch the active API key by name."""
    if not set_active_key(body.name):
        raise HTTPException(status_code=404, detail=f"Key '{body.name}' not found.")
    # Bust cache so next requests use the new key's quota
    _cache.clear()
    return {"active": get_active_key_name(), "message": f"Switched to '{body.name}'. Cache cleared."}
