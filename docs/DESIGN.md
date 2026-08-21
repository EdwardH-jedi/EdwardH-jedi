# Edward Profile / Developer Hub Visual System

## Core direction

**Computational Editorial × Human Micro-Motion**

The visual language should feel like a technical publication that has quietly come alive. It is precise, restrained, evidence-aware, and slightly experimental. The goal is not to look like a generic developer landing page, a cyberpunk dashboard, or a badge wall.

## Ratio

- 65% precise modern engineering interface
- 35% experimental computational art

## Tone

- dark warm-black surfaces
- warm gray typography and line work
- one restrained mint/teal signal accent
- hairline grids and structural separators
- mono labels for system metadata
- sans-serif display type for names / major headings
- irregularity should come from composition and motion, not decoration

## Current palette

- background: `#0a0d0e`
- elevated surface: `#101517` / `#11181a`
- primary text: `#f1efe8`
- secondary text: `#8e999c` / `#9ca6a9`
- muted text: `#657174`
- grid / hairline: `#30383b`
- active signal: `#78d0c8`

Keep the accent sparse. It indicates active flow, current state, selected nodes, or evidence-bearing signal.

## Typography

### Editorial display

Use a clean sans-serif for major naming and identity moments.

### System metadata

Use a mono stack:

```text
ui-monospace, SFMono-Regular, Menlo, Consolas, monospace
```

Examples:

```text
AIML—01 / AFL PREDICT
PUBLIC SIGNAL / PUBLIC GITHUB
TEST / QUALITY
SOURCE-FIRST
```

## Human Micro-Motion

Characters are intentionally simple articulated line figures. They should feel observational and human, not cute, mascot-like, or corporate-illustration-like.

### Rules

- warm-gray strokes
- small head circle
- simple articulated torso / limbs
- subtle weight shifts
- asynchronous timing between figures
- tiny pauses and anticipation
- no teleporting
- no perfectly synchronized group movement
- no exaggerated squash/stretch
- no emoji faces

### Motion timing

- main loops: approximately 5–10 seconds
- signal pulses: approximately 2.5–3.5 seconds
- moving dashes / data flow: approximately 3.5–6 seconds
- motion should remain understandable on a static frame

### Reduced motion

Every animated SVG or Three.js implementation must support `prefers-reduced-motion: reduce`.

For reduced motion:

- remove continuous loops
- keep the strongest representative static frame
- preserve all labels and structural relationships

## Project choreography

### AFL Predict

The models are **predictive models, not AI agents**.

Use:

```text
ELO
LOGISTIC
XGBOOST
POISSON
       ↓
weighted ENSEMBLE
       ↓
final prediction
       ↓
outcome check
```

Optional Bookmaker representation is acceptable only when useful to the exact evaluated system. Do not invent weights or probabilities.

### Wardrobe

Use:

```text
garment
  ↓
local archive
  ↓
outfit composition
  ↓
proxy 3D experiment
```

Never visually imply true virtual try-on, cloth simulation, body fitting, or garment reconstruction.

### Protin

Use:

```text
individual activity
  ↓
discovery
  ↓
match / join
  ↓
group session
```

Avoid fitness-ad visual language. The focus is social discovery and coordination.

### Walkroo

Future choreography:

```text
person + dog
  ↓
walk
  ↓
route trace
  ↓
place marker
```

Dog movement should include small pauses, direction changes, or sniff moments.

### PanSegAI

Future choreography:

```text
medical image
  ↓
model/process
  ↓
segmentation region
  ↓
comparison
```

No fake Dice score, accuracy, clinical deployment, or unsupported claims.

## Engineering Landscape

The landscape is a spatial representation of engineering systems, not a game map.

### Semantic layout

- AFL Predict → ML / evaluation district
- Wardrobe → product / local-first district
- Protin → backend / mobile district
- GitHub Brain → future system core
- Developer Hub → presentation / navigation layer

### Future Three.js behavior

- drag → rotate
- subtle inertial camera movement
- hover → project highlight and concise signal
- click → project case study / detail
- optional recent-activity pulse per project
- optional edges from GitHub Brain to indexed projects
- no free-fly first-person camera
- no game HUD
- no giant glowing particles

## Things to avoid

Do not introduce:

- purple gradients
- glassmorphism
- neon cyberpunk glow
- generic SaaS bento grids
- fake terminal windows
- skill percentage bars
- excessive GitHub badges
- typing-animation clichés
- decorative particle fields
- fake numerical metrics
- unverified AI claims
- invented repo status

## Evidence language

The design system is part of the evidence model.

Status and claim language should distinguish:

```text
PUBLIC
PRIVATE BUILD
LOCAL EVIDENCE
ACADEMIC / IN PROGRESS
BUILDING
EXPERIMENTAL
```

A private project must never be made to look publicly inspectable.

## Shared principle

**Build the system. Test the claim. Show the evidence.**
