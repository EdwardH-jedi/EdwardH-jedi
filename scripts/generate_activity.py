#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from urllib import parse, request
from urllib.error import HTTPError, URLError
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"

USERNAME = os.getenv("PROFILE_USERNAME", "EdwardH-jedi")
TOKEN = os.getenv("GITHUB_TOKEN", "")
API = "https://api.github.com"
LOCAL_TZ = ZoneInfo(os.getenv("PROFILE_TIMEZONE", "Australia/Sydney"))
WINDOW_DAYS = 30
MAX_REPOS = 5
MAX_LATEST = 3
MAX_COMMITS_PER_REPO = 40

CATEGORY_RULES = [
    ("TEST / QUALITY", ("test", "pytest", "lint", "typecheck", "coverage", "quality", "ruff")),
    ("ML / EVALUATION", ("model", "train", "eval", "evaluation", "calibrat", "predict", "xgboost", "brier", "log loss")),
    ("SYSTEMS / OPS", ("deploy", "docker", "linux", "workflow", "action", " ci ", "server", "infra")),
    ("FIX / RELIABILITY", ("fix", "bug", "reliab", "crash", "error", "recover", "safety")),
    ("ARCHITECTURE", ("refactor", "architect", "persist", "migration", "storage", "schema", "pipeline")),
    ("PRODUCT / FEATURE", ("feat", "feature", "implement", "add ", " ui ", " ux ", "screen", "flow")),
    ("DOCS / EVIDENCE", ("docs", "readme", "portfolio", "evidence", "document")),
]


def api_get(path: str):
    req = request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "edward-profile-activity",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def clean(text: str, limit: int = 100) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def parse_date(value: str) -> dt.datetime | None:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None


def display_date(value: str) -> str:
    parsed = parse_date(value)
    if not parsed:
        return "—"
    return parsed.astimezone(LOCAL_TZ).strftime("%d %b").upper()


def item_display_date(item: dict) -> str:
    return clean(str(item.get("display_date") or item.get("date") or "—"), 16).upper()


def classify(message: str) -> str:
    lowered = f" {message.lower()} "
    for category, needles in CATEGORY_RULES:
        if any(needle in lowered for needle in needles):
            return category
    return "ENGINEERING"


def meaningful(message: str) -> bool:
    lowered = (message or "").strip().lower()
    if not lowered:
        return False
    if lowered.startswith("merge "):
        return False
    if lowered.startswith("chore(profile):"):
        return False
    if "[skip profile]" in lowered:
        return False
    return True


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

    items = []
    for item in payload.get("items", []):
        if not isinstance(item, dict):
            continue
        if item.get("public_safe") is not True:
            continue
        if item.get("source_visibility") != "public":
            continue
        repo = clean(str(item.get("repo", "")), 40)
        summary = clean(str(item.get("summary", "")), 110)
        category = clean(str(item.get("category", "EVIDENCE UPDATE")), 30)
        date = clean(str(item.get("date", "")), 16).upper() or "—"
        source_url = clean(str(item.get("source_url", "")), 180)
        if repo and summary and source_url.startswith("https://github.com/"):
            items.append({
                "repo": repo,
                "summary": summary,
                "category": category,
                "date": date,
                "source_url": source_url,
            })
        if len(items) >= MAX_LATEST:
            break
    return items or None


def public_repositories():
    repos = api_get(
        f"/users/{parse.quote(USERNAME)}/repos"
        "?per_page=100&sort=pushed&direction=desc&type=owner"
    )
    result = []
    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        if repo.get("name") == USERNAME:
            continue
        if repo.get("private") is True or repo.get("visibility") not in (None, "public"):
            continue
        result.append(repo)
    return result


# Edward commits under two GitHub accounts. The signal counts commits authored
# by either, and nobody else's — a collaborator's commit on one of these
# repositories is not evidence of Edward's activity.
OWNED_AUTHOR_LOGINS = frozenset(
    login.strip().lower()
    for login in os.environ.get(
        "PROFILE_AUTHOR_LOGINS", "EdwardH-jedi,edwardhwang1223-crypto"
    ).split(",")
    if login.strip()
)


def authored_by_owner(raw: dict) -> bool:
    """True when GitHub attributes the commit to one of the owner's accounts.

    Commits with no linked account are excluded: without a login there is no
    way to tell the owner's work from a contributor's.
    """
    author = raw.get("author")
    if not isinstance(author, dict):
        return False
    login = author.get("login")
    return isinstance(login, str) and login.lower() in OWNED_AUTHOR_LOGINS


def recent_commits(repo_name: str, since: dt.datetime):
    since_iso = since.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    query = parse.urlencode({"since": since_iso, "per_page": MAX_COMMITS_PER_REPO})
    try:
        payload = api_get(
            f"/repos/{parse.quote(USERNAME)}/{parse.quote(repo_name)}/commits?{query}"
        )
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return []

    commits = []
    for raw in payload:
        if not authored_by_owner(raw):
            continue
        commit = raw.get("commit", {})
        message = (commit.get("message") or "").splitlines()[0]
        if not meaningful(message):
            continue
        date_value = (
            commit.get("committer", {}).get("date")
            or commit.get("author", {}).get("date")
            or ""
        )
        if not parse_date(date_value):
            continue
        commits.append({
            "repo": repo_name,
            "summary": clean(message, 110),
            "category": classify(message),
            "date": date_value,
            "display_date": display_date(date_value),
            "sha": raw.get("sha", "")[:10],
            "url": raw.get("html_url", ""),
        })
    return commits


def collect_public_activity(now_utc: dt.datetime):
    since = now_utc - dt.timedelta(days=WINDOW_DAYS)
    commits = []
    repo_meta = {}
    for repo in public_repositories():
        name = repo.get("name", "")
        if not name:
            continue
        repo_meta[name] = {
            "pushed_at": repo.get("pushed_at"),
            "language": repo.get("language"),
            "url": repo.get("html_url"),
        }
        commits.extend(recent_commits(name, since))

    commits.sort(
        key=lambda item: parse_date(item["date"]) or dt.datetime.min.replace(tzinfo=dt.timezone.utc),
        reverse=True,
    )
    return commits, repo_meta


# Engineering state, derived only from owned public commits in the window.
#
# The thresholds are deliberate and deterministic — no model, and no inference
# about what Edward is "doing". The signal reports only what it can observe:
# commits authored by the owner on their own public repositories. It says
# nothing about private work, because it cannot see any.
STATE_RULES = (
    # (minimum commits in window, state, one-line meaning)
    (12, "SHIPPING", "sustained public commit activity across repositories"),
    (6, "BUILDING", "steady public commits in the window"),
    (3, "FIXING", "a few focused public changes"),
    (1, "QUIET", "few public commits in this window"),
    (0, "QUIET", "no public commits in this window"),
)


def engineering_state(commit_count: int) -> tuple[str, str]:
    """Map a commit count to a state and its explanation. Purely deterministic."""
    for threshold, state, meaning in STATE_RULES:
        if commit_count >= threshold:
            return state, meaning
    return "QUIET", "no public commits in the window"


def summarize(commits, now_local: dt.datetime):
    repo_counts = Counter(item["repo"] for item in commits)
    category_counts = Counter(item["category"] for item in commits)

    week_start = now_local - dt.timedelta(days=now_local.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start_utc = week_start.astimezone(dt.timezone.utc)
    weekly = [
        item for item in commits
        if (parse_date(item["date"]) or dt.datetime.min.replace(tzinfo=dt.timezone.utc)) >= week_start_utc
    ]
    weekly_repo_counts = Counter(item["repo"] for item in weekly)
    weekly_category_counts = Counter(item["category"] for item in weekly)

    return {
        "repo_counts": repo_counts,
        "category_counts": category_counts,
        "weekly": weekly,
        "weekly_repo_counts": weekly_repo_counts,
        "weekly_category_counts": weekly_category_counts,
        "top_repos": [name for name, _ in repo_counts.most_common(MAX_REPOS)],
        "state": engineering_state(len(commits))[0],
        "state_meaning": engineering_state(len(commits))[1],
        "commit_total": len(commits),
    }


def escape(value) -> str:
    return html.escape(str(value), quote=True)


def split_svg_text(text: str, width: int = 54):
    words = clean(text, 110).split()
    if not words:
        return [""]
    lines = [words[0]]
    for word in words[1:]:
        if len(lines[-1]) + 1 + len(word) <= width:
            lines[-1] += " " + word
        elif len(lines) < 2:
            lines.append(word)
        else:
            lines[-1] = clean(lines[-1] + " " + word, width)
            break
    return lines[:2]


def render_signal_strip(summary, commits, source: str, generated: str) -> str:
    """One-line signal strip: state, meaning, window, and where it came from.

    Replaces the full-height timeline plate. The same numbers, at a size that
    matches how much they actually tell a reader.
    """
    repos = len(summary["repo_counts"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 64" width="900" height="64" role="img" aria-label="Public engineering signal: state {escape(summary["state"])}, {len(commits)} commits across {repos} public repositories in the last 30 days. Private repositories are excluded.">
  <title>Public engineering signal</title>
  <style>.m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}</style>
  <rect width="900" height="64" rx="6" fill="#0a0d0e"/>
  <rect x="14" y="14" width="3" height="36" rx="1.5" fill="#78d0c8"/>
  <text class="m" x="30" y="28" font-size="9" letter-spacing="1.4" fill="#8b9498">PUBLIC SIGNAL / LAST {WINDOW_DAYS} DAYS</text>
  <text class="m" x="30" y="45" font-size="11" letter-spacing="1.2" fill="#f1efe8">{escape(summary["state"])}</text>
  <text class="m" x="96" y="45" font-size="9" letter-spacing="0.6" fill="#8b9498">{escape(summary["state_meaning"])}</text>
  <text class="m" x="886" y="28" text-anchor="end" font-size="9" letter-spacing="1.1" fill="#78d0c8">{len(commits)} COMMITS / {repos} REPOS</text>
  <text class="m" x="886" y="45" text-anchor="end" font-size="8" letter-spacing="1" fill="#8b9498">{escape(source)} · {escape(generated)}</text>
</svg>
'''


def stable_generated_at(core_payload: dict, now_local: dt.datetime):
    # The rendered day is included: dot positions are day-relative, so a new day
    # legitimately changes the plate even when the commit set has not. Without
    # this the fingerprint would claim nothing changed while the SVG had.
    canonical = json.dumps(
        {**core_payload, "rendered_on": now_local.date().isoformat()},
        sort_keys=True,
        separators=(",", ":"),
    )
    fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    previous = {}
    path = DATA / "activity.json"
    if path.exists():
        try:
            previous = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            previous = {}

    if previous.get("fingerprint") == fingerprint and previous.get("generated_at"):
        generated_at = previous["generated_at"]
    else:
        generated_at = now_local.strftime("%Y-%m-%d %H:%M %Z")
    return fingerprint, generated_at


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    now_utc = dt.datetime.now(dt.timezone.utc)
    now_local = now_utc.astimezone(LOCAL_TZ)

    try:
        commits, repo_meta = collect_public_activity(now_utc)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        # Fail closed. An empty result from a transient GitHub failure is
        # indistinguishable from a genuinely quiet window, and writing it would
        # publish a fabricated QUIET state and commit it to main. Leave the last
        # good signal in place instead.
        print(f"GitHub request failed ({error}); leaving the existing signal untouched.")
        return 1

    summary = summarize(commits, now_local)
    brain_items = load_brain_items()
    if brain_items:
        latest_items = brain_items
        source = "GITHUB BRAIN / PUBLIC_SAFE"
    else:
        latest_items = commits[:MAX_LATEST]
        source = "PUBLIC GITHUB"

    core_payload = {
        "window_days": WINDOW_DAYS,
        "public_safe": True,
        "source": source,
        "commits": commits,
        "latest": latest_items,
        "repo_counts": dict(summary["repo_counts"]),
        "category_counts": dict(summary["category_counts"]),
        "weekly_repo_counts": dict(summary["weekly_repo_counts"]),
        "weekly_category_counts": dict(summary["weekly_category_counts"]),
        "repo_meta": repo_meta,
        "state": summary["state"],
        "state_meaning": summary["state_meaning"],
    }
    fingerprint, generated = stable_generated_at(core_payload, now_local)

    (ASSETS / "signal-strip.svg").write_text(
        render_signal_strip(summary, commits, source, generated),
        encoding="utf-8",
    )
    (DATA / "activity.json").write_text(
        json.dumps({"generated_at": generated, "fingerprint": fingerprint, **core_payload}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Rendered {len(commits)} public commit signal(s) over {WINDOW_DAYS} days, "
        f"{len(summary['repo_counts'])} active repo(s), state={summary['state']}, source={source}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
