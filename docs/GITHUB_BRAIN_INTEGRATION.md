# GitHub Brain → Profile contract

The profile repository is public. GitHub Brain may enrich the generated activity card only through `data/brain.json`, and only when the payload contains `"public_safe": true`.

## Safety boundary

- `public_safe` must be exactly `true`.
- `data/brain.json` itself is public and must never contain private source text, private repository names, secrets, tokens, local file paths, or unpublished claims.
- The fallback renderer uses GitHub's public user repository surface, so automatic repository discovery is limited to public repositories.
- GitHub Brain should generate a proposal from evidence, validate that the evidence is public, and only then write or propose `data/brain.json`.
- Curated biography, experience, education, and project claims remain human-owned. Automation updates the activity artifact only.

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
data/brain.json
        ↓
profile activity renderer
```

## Current state

Until GitHub Brain is connected, `scripts/generate_activity.py` uses public GitHub repository and commit metadata as a fallback. The generated `assets/activity.svg` is refreshed by GitHub Actions.
