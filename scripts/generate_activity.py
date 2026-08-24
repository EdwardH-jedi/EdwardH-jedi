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


def plural_changes(count: int) -> str:
    return f"{count} change" if count == 1 else f"{count} changes"


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
# The thresholds are deliberate and deterministic — no model, no inference about
# what Edward is "doing". When public activity is thin the state is QUIET, which
# is the honest reading: most work in a given week may be happening in private
# repositories that this signal cannot and should not see.
STATE_RULES = (
    # (minimum commits in window, state, one-line meaning)
    (12, "SHIPPING", "sustained public commit activity across repositories"),
    (6, "BUILDING", "steady public commits in the window"),
    (3, "FIXING", "small, focused public changes"),
    (1, "QUIET", "little public activity — current work is not public"),
    (0, "QUIET", "no public commits in the window"),
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


def render_activity_svg(commits, summary, latest_items, source: str, generated: str, now_utc: dt.datetime):
    chart_x0, chart_x1 = 180, 735
    chart_w = chart_x1 - chart_x0
    chart_y0, lane_gap = 112, 56
    since = now_utc - dt.timedelta(days=WINDOW_DAYS)

    lane_parts = []
    top_repos = summary["top_repos"][:MAX_REPOS]
    by_repo = defaultdict(list)
    for item in commits:
        by_repo[item["repo"]].append(item)

    for idx, repo in enumerate(top_repos):
        y = chart_y0 + idx * lane_gap
        lane_parts.append(f'<text x="42" y="{y+4}" class="m" fill="#e8e8e3" font-size="12">{escape(repo)}</text>')
        lane_parts.append(f'<text x="151" y="{y+4}" text-anchor="end" class="m" fill="#657174" font-size="10">{len(by_repo[repo])}</text>')
        lane_parts.append(f'<line x1="{chart_x0}" y1="{y}" x2="{chart_x1}" y2="{y}" stroke="#273034"/>')

        repo_items = sorted(by_repo[repo], key=lambda item: parse_date(item["date"]) or since)
        for c_idx, item in enumerate(repo_items):
            when = parse_date(item["date"]) or since
            fraction = (when - since).total_seconds() / max((now_utc - since).total_seconds(), 1)
            fraction = max(0.0, min(1.0, fraction))
            x = chart_x0 + fraction * chart_w
            cls = "dot hot" if c_idx == len(repo_items) - 1 else "dot"
            lane_parts.append(
                f'<circle cx="{x:.1f}" cy="{y}" r="4.2" class="{cls}"><title>{escape(item["display_date"])} · {escape(item["summary"])}</title></circle>'
            )

    if not top_repos:
        lane_parts.append('<text x="42" y="150" class="m" fill="#8e999c" font-size="12">No public commit activity was available in the 30-day window.</text>')

    latest_parts = []
    for idx, item in enumerate(latest_items[:MAX_LATEST]):
        y = 118 + idx * 96
        latest_parts.append(f'<text x="790" y="{y}" class="m" fill="#78d0c8" font-size="10">{escape(item_display_date(item))}</text>')
        latest_parts.append(f'<text x="866" y="{y}" class="m" fill="#f1efe8" font-size="12">{escape(item["repo"])}</text>')
        latest_parts.append(f'<text x="1158" y="{y}" text-anchor="end" class="m" fill="#657174" font-size="9">{escape(item.get("category", "ENGINEERING"))}</text>')
        lines = split_svg_text(item["summary"], 43)
        latest_parts.append(f'<text x="790" y="{y+24}" class="m" fill="#9aa5a8" font-size="10">{escape(lines[0])}</text>')
        if len(lines) > 1:
            latest_parts.append(f'<text x="790" y="{y+41}" class="m" fill="#9aa5a8" font-size="10">{escape(lines[1])}</text>')
        if idx < MAX_LATEST - 1:
            latest_parts.append(f'<line x1="790" y1="{y+62}" x2="1158" y2="{y+62}" stroke="#232a2d"/>')

    if not latest_parts:
        latest_parts.append('<text x="790" y="140" class="m" fill="#8e999c" font-size="11">No public-safe latest signal.</text>')

    tick_parts = []
    for days_ago, label in ((30, "30D AGO"), (20, "20D"), (10, "10D"), (0, "NOW")):
        fraction = (WINDOW_DAYS - days_ago) / WINDOW_DAYS
        x = chart_x0 + fraction * chart_w
        tick_parts.append(f'<line x1="{x:.1f}" y1="82" x2="{x:.1f}" y2="390" stroke="#171d1f"/>')
        tick_parts.append(f'<text x="{x:.1f}" y="70" text-anchor="middle" class="m" fill="#5f6b6e" font-size="9">{label}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470" role="img" aria-labelledby="title desc">
  <title id="title">Edward Hwang live public engineering signal</title>
  <desc id="desc">Thirty-day public GitHub activity timeline and latest meaningful public work.</desc>
  <style>
    .m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
    .dot{{fill:#7b878a;opacity:.72}}
    .hot{{fill:#78d0c8;animation:pulse 2.8s ease-in-out infinite}}
    @keyframes pulse{{0%,100%{{opacity:.42}}50%{{opacity:1}}}}
    @media (prefers-reduced-motion:reduce){{.hot{{animation:none;opacity:1}}}}
  </style>
  <rect width="1200" height="470" rx="10" fill="#0a0d0e"/>
  <path d="M38 54H1162M38 410H1162" stroke="#30383b"/>
  <line x1="760" y1="72" x2="760" y2="390" stroke="#30383b"/>
  <text x="38" y="34" class="m" fill="#778286" font-size="12" letter-spacing="2">LIVE ENGINEERING SIGNAL / LAST 30 DAYS</text>
  <text x="1162" y="34" text-anchor="end" class="m" fill="#78d0c8" font-size="10">SOURCE / {escape(source)}</text>
  <text x="42" y="74" class="m" fill="#657174" font-size="9" letter-spacing="1.4">PUBLIC REPOSITORY ACTIVITY</text>
  <text x="790" y="74" class="m" fill="#657174" font-size="9" letter-spacing="1.4">LATEST MEANINGFUL WORK</text>
  {''.join(tick_parts)}
  {''.join(lane_parts)}
  {''.join(latest_parts)}
  <text x="38" y="440" class="m" fill="#657174" font-size="9" letter-spacing="1.05">UPDATED {escape(generated)} · DOTS = PUBLIC COMMITS ON OWNED PUBLIC REPOSITORIES · PRIVATE REPOSITORIES ARE EXCLUDED.</text>
  <circle cx="1152" cy="437" r="4" fill="#78d0c8" class="hot"/>
</svg>
'''


def stable_generated_at(core_payload: dict, now_local: dt.datetime):
    canonical = json.dumps(core_payload, sort_keys=True, separators=(",", ":"))
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
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        commits, repo_meta = [], {}

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

    (ASSETS / "activity.svg").write_text(
        render_activity_svg(commits, summary, latest_items, source, generated, now_utc),
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


if __name__ == "__main__":
    main()
