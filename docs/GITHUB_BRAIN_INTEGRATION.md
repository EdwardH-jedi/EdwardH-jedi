# GitHub Brain → Profile contract

This profile repository is public. GitHub Brain may enrich the generated `LATEST MEANINGFUL WORK` surface only through `data/brain.json`.

The activity timeline and weekly counts remain derived from owned public GitHub repository metadata. Brain output may replace the natural-language summary only after it passes the public evidence gate below.

## Required gate

The root payload must contain:

```json
{
  "public_safe": true
}
```

Every item must also contain:

```json
{
  "public_safe": true,
  "source_visibility": "public",
  "source_url": "https://github.com/..."
}
```

If any of these checks fail, that item is ignored and the renderer falls back to public GitHub commit metadata.

## Safety boundary

- `data/brain.json` is itself public.
- Never write private repository names, private source text, secrets, tokens, local paths, unpublished claims, or internal-only evidence into it.
- `source_visibility` must be exactly `"public"`.
- `source_url` must point to a GitHub public evidence surface.
- Brain summaries must be evidence-backed and conservative.
- Curated biography, education, employment history, awards, and core project claims remain human-owned.
- Automation updates only generated activity/focus artifacts unless a separate human-approved profile PR is created.

## Intended flow

```text
GitHub repositories
        ↓
GitHub Brain local index
        ↓
evidence selection
        ↓
public/private policy
        ↓
public-safe summary proposal
        ↓
public_safe + source_visibility checks
        ↓
data/brain.json
        ↓
profile signal renderer
```

## Current state

Until GitHub Brain is connected, `scripts/generate_activity.py` uses owned public repository and commit metadata as the fallback source.

GitHub Actions checks every six hours. A content fingerprint prevents timestamp-only commits when the underlying public signal has not changed.
