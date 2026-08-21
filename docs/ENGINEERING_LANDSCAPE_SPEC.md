# Engineering Landscape — Implementation Contract

This document defines the handoff boundary between the GitHub Profile surfaces and the future interactive Developer Hub implementation.

## Goal

Create a real interactive Three.js engineering landscape that extends the GitHub Profile pseudo-3D teaser without redesigning the Developer Hub.

The experience should communicate:

- what systems Edward is building
- how those systems relate to engineering domains
- which systems have public evidence
- which systems are private, local, academic, or experimental
- what changed recently, when public-safe data exists

## Source of truth

The implementation must follow:

1. `docs/DESIGN.md`
2. existing Developer Hub design tokens and layout
3. curated project metadata in the Developer Hub
4. public-safe activity data only

Do not let the Three.js scene become a separate visual brand.

## Scene model

Suggested logical nodes:

```text
AFL Predict
- id: afl-predict
- domain: ml-evaluation
- visibility: public
- publicEvidence: true

Wardrobe
- id: wardrobe
- domain: product-local-first
- visibility: public
- publicEvidence: true
- experimental: proxy-3d

Protin
- id: protin
- domain: backend-mobile
- visibility: public
- publicEvidence: true

Developer Hub
- id: developer-hub
- domain: presentation-system
- visibility: private-build
- publicEvidence: false

GitHub Brain
- id: github-brain
- domain: local-ai-infrastructure
- visibility: building
- publicEvidence: false until a public repository/evidence surface exists

PanSegAI
- id: pansegai
- domain: ml-research
- visibility: academic-in-progress
- publicEvidence: false unless explicitly verified
```

## Required data contract

The Three.js layer should consume structured project data, not hard-coded labels spread across scene components.

Minimum shape:

```ts
export type LandscapeProject = {
  id: string;
  name: string;
  domain: string;
  status: string;
  visibility: "public" | "private-build" | "local-evidence" | "academic" | "building";
  publicEvidence: boolean;
  href?: string;
  tech?: string[];
  latestActivity?: {
    summary: string;
    category: string;
    date: string;
    sourceUrl?: string;
    sourceVisibility: "public";
    publicSafe: true;
  };
};
```

## Public safety rules

Interactive UI must not imply that a private/local project is publicly inspectable.

Activity can appear publicly only when:

```text
publicSafe === true
sourceVisibility === "public"
sourceUrl points to an approved public GitHub source
```

Never display:

- private repository names not already curated for public display
- private source paths
- local filesystem paths
- tokens / secrets
- private issue or PR content
- unpublished metrics
- model claims without public evidence

## Interaction requirements

### Desktop

- drag → orbit / rotate
- wheel or trackpad → restrained zoom
- hover → highlight project node
- hover panel → name, domain, status, concise latest public-safe signal when available
- click → navigate to corresponding Developer Hub project case study or project detail

### Mobile

Do not force precision 3D interaction.

Provide either:

- reduced camera controls with tap targets, or
- static/isometric landscape fallback with vertically stacked project cards

No horizontal overflow.

## Motion

- subtle idle motion only
- different project nodes should not bob in sync
- activity signal may pulse only on projects with recent public-safe activity
- GitHub Brain edges may animate only after the system actually has evidence relationships to render

Support `prefers-reduced-motion`.

## Performance requirements

Target modern laptop / desktop smoothness.

Recommended acceptance targets:

- avoid unnecessary continuous React state updates per frame
- cap DPR where useful
- resize through ResizeObserver
- dispose geometries/materials/textures on unmount
- lazy-load Three.js scene if it is below the fold
- no uncontrolled post-processing stack
- no large textures for simple editorial surfaces

## Accessibility

- Three.js canvas must not be the only way to access project links
- provide semantic fallback links/cards
- keyboard users must be able to reach all project destinations
- project hover information must also be available on focus
- reduced motion must preserve meaning

## Visual acceptance criteria

PASS only if the scene:

- looks like an extension of the computational editorial site
- uses the warm-gray + restrained mint system
- has readable project hierarchy
- does not look like a cyberpunk dashboard
- avoids generic floating cubes unless they encode a project/domain relationship
- contains no fake metrics
- contains no fake live status
- preserves existing site typography and spacing language

## Functional acceptance criteria

PASS only if:

- drag/orbit works on desktop
- hover/focus project highlighting works
- click navigation works
- mobile fallback works
- reduced-motion behavior works
- private/public presentation rules are preserved
- project data comes from structured data rather than scattered hard-coded JSX
- build/typecheck/lint/tests pass

## Explicitly out of scope for this phase

- GitHub Brain implementation
- local MLX model runtime
- RAG indexing
- automatic portfolio PR generation
- public chatbot
- RTX worker integration
- advanced physics
- true 3D contribution graph clone

The Three.js landscape is a presentation layer. GitHub Brain comes later as a separate implementation phase.
