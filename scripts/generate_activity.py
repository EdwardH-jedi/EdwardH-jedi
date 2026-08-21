#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import json
import os
from pathlib import Path
from urllib import parse, request
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
USERNAME = os.getenv("PROFILE_USERNAME", "EdwardH-jedi")
TOKEN = os.getenv("GITHUB_TOKEN", "")
API = "https://api.github.com"
MAX_ITEMS = 4


def api_get(path: str):
    req = request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "edward-profile-activity",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def clean(text: str, limit: int = 92) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def format_date(value: str) -> str:
    try:
        stamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return stamp.strftime("%d %b").upper()
    except Exception:
        return "—"


def load_brain_items():
    path = DATA / "brain.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("public_safe") is not True:
        return None
    raw_items = payload.get("items")
    if not isinstance(raw_items, list):
        return None
    items = []
    for item in raw_items[:MAX_ITEMS]:
        if not isinstance(item, dict):
            continue
        repo = clean(str(item.get("repo", "")), 40)
        summary = clean(str(item.get("summary", "")), 92)
        category = clean(str(item.get("category", "EVIDENCE UPDATE")), 30)
        date = clean(str(item.get("date", "")), 16)
        if repo and summary:
            items.append({"repo": repo, "summary": summary, "category": category, "date": date.upper() if date else "—"})
    return items or None


def load_public_github_items():
    repos = api_get(f"/users/{parse.quote(USERNAME)}/repos?per_page=100&sort=pushed&direction=desc")
    items = []
    for repo in repos:
        if len(items) >= MAX_ITEMS:
            break
        if repo.get("fork") or repo.get("archived") or repo.get("name") == USERNAME:
            continue
        if repo.get("private") is True or repo.get("visibility") not in (None, "public"):
            continue
        name = repo.get("name", "")
        branch = repo.get("default_branch") or "main"
        message = ""
        date_value = repo.get("pushed_at") or ""
        try:
            commits = api_get(f"/repos/{parse.quote(USERNAME)}/{parse.quote(name)}/commits?sha={parse.quote(branch)}&per_page=1")
            if commits:
                commit = commits[0].get("commit", {})
                message = (commit.get("message") or "").splitlines()[0]
                date_value = commit.get("committer", {}).get("date") or commit.get("author", {}).get("date") or date_value
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            pass
        items.append({"repo": clean(name, 40), "summary": clean(message or "public repository activity", 92), "category": "PUBLIC COMMIT", "date": format_date(date_value)})
    return items


def render_svg(items, source: str, generated: str) -> str:
    rows = []
    for idx, item in enumerate(items[:MAX_ITEMS]):
        y = 92 + idx * 68
        rows.append(f'''\n    <text x="46" y="{y}" fill="#78d0c8">{html.escape(item["date"])}</text>\n    <text x="154" y="{y}" fill="#f1efe8" font-size="14">{html.escape(item["repo"])}</text>\n    <text x="154" y="{y + 21}" fill="#8e999c">{html.escape(item["summary"])}</text>\n    <text x="1128" y="{y}" text-anchor="end" fill="#657174">{html.escape(item.get("category", "PUBLIC COMMIT"))}</text>\n    <line x1="46" y1="{y + 36}" x2="1154" y2="{y + 36}" stroke="#232a2d"/>''')
    if not rows:
        rows.append('\n    <text x="46" y="112" fill="#8e999c">No public activity was available at render time.</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="390" viewBox="0 0 1200 390" role="img" aria-labelledby="title desc">\n  <title id="title">Recent public engineering activity</title>\n  <desc id="desc">Public-safe GitHub engineering activity for {html.escape(USERNAME)}.</desc>\n  <style>.m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}</style>\n  <rect width="1200" height="390" rx="10" fill="#0a0d0e"/>\n  <path d="M38 54H1162M38 348H1162" stroke="#30383b"/>\n  <text x="38" y="34" class="m" fill="#778286" font-size="12" letter-spacing="2">RECENT ENGINEERING ACTIVITY / PUBLIC SURFACE</text>\n  <text x="1162" y="34" text-anchor="end" class="m" fill="#78d0c8" font-size="11">SOURCE / {html.escape(source)}</text>\n  <g class="m" font-size="11">{''.join(rows)}\n  </g>\n  <text x="38" y="374" class="m" fill="#657174" font-size="10" letter-spacing="1.1">GENERATED {html.escape(generated)} UTC · PRIVATE REPOSITORIES ARE NOT ELIGIBLE FOR FALLBACK RENDERING.</text>\n</svg>\n'''


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    brain_items = load_brain_items()
    if brain_items:
        items, source = brain_items, "GITHUB BRAIN / PUBLIC_SAFE"
    else:
        try:
            items = load_public_github_items()
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            items = []
        source = "PUBLIC GITHUB FALLBACK"
    (ASSETS / "activity.svg").write_text(render_svg(items, source, generated), encoding="utf-8")
    (DATA / "activity.json").write_text(json.dumps({"generated_at": generated + "Z", "source": source, "public_safe": True, "items": items}, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(items)} public-safe activity item(s) from {source}.")


if __name__ == "__main__":
    main()
