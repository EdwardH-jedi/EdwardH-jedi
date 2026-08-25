<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img src="assets/banner-light.svg" alt="Edward Hwang — ML systems and shipped software, Sydney">
</picture>

Final-year Computer Science at the University of Sydney. I build ML systems and measure them — then ship the ones that hold up.

`Sydney, AU` · [Email](mailto:edwardhwang1223@gmail.com) · [LinkedIn](https://linkedin.com/in/YOUR-HANDLE) · Open to graduate software engineering roles from December 2026

---

## Now

- **Protin** — matchmaking and ranking flows; latest push 25 Aug.
- **AFL Predict** — GPU-accelerated Optuna sweeps on the ensemble, odds collection running nightly against a Postgres spine.
- **The Archive** — 3-way cutout benchmark on the `eval/cutout-bench` branch, and a trimesh procedural mannequin replacing the dummy avatar builder.
- Pancreas segmentation capstone for an external client. Private repo while the work is in progress.

---

## Selected work

### Protin — peer sports matchmaking
Find opponents by sport, issue challenges, book nearby courts, track results through a ranking and honour system.

| | |
|---|---|
| **Scope** | Full-stack mobile: matchmaking, challenges, court booking, ranking and honour system |
| **Stack** | React Native · Expo · TypeScript · FastAPI · SQLAlchemy · PostgreSQL · Redis · Docker · pytest |
| **Status** | Active — largest codebase here |

→ [`EdwardH-jedi/Protin`](https://github.com/EdwardH-jedi/Protin)

### AFL Predict — paper-trading research system
Scheduled ingestion, temporal feature engineering, calibrated ensemble models, walk-forward backtesting, FastAPI service.

| | |
|---|---|
| **Evidence** | 13 feature extractors · 6 model types · walk-forward backtest harness · closing-line-value tracking |
| **Honest limit** | Paper trading only. No live betting, no money placed, no claimed edge. |
| **Infrastructure** | Three machines by role — a 24/7 Postgres spine, an RTX 5080 training box, a laptop cockpit. Collection scheduled around a 500-call monthly API quota. |
| **Stack** | Python · XGBoost · SHAP · FastAPI · React · PostgreSQL |
| **Status** | Backtested, not live |

→ [`EdwardH-jedi/AFL_predict`](https://github.com/EdwardH-jedi/AFL_predict)

### The Archive — local-first wardrobe with a measured vision pipeline
Browser-persisted garment archive, outfit composition, and a scoped proxy-3D experiment. An iOS client shares the same domain model.

| | |
|---|---|
| **Evidence** | 378 frontend tests · 52 backend pytest tests · async `/api/jobs` lifecycle behind 5 named interfaces |
| **Benchmark** | The cutout engine was chosen by measurement, not preference. Vision on-device subject lifting beat flood fill on flat-lay images, 18 of 22. The failures that remain are fine interior gaps — lace, fringe — which is why YOLOv11-seg stays on the bench instead of in the pipeline. |
| **Stack** | React · TypeScript · Vite · Three.js · Vitest · FastAPI · trimesh · Swift / SwiftUI |
| **Status** | Active — web and iOS clients exchange archives via export and import |

→ [`EdwardH-jedi/wadrobe`](https://github.com/EdwardH-jedi/wadrobe)

---

## Stack

**Backend** Python · FastAPI · PostgreSQL / pgvector · Redis · Docker
**Frontend** React · TypeScript · Vite · React Native / Expo · SwiftUI
**ML** PyTorch · XGBoost · SHAP · YOLO · MONAI
**Systems** C · Linux / bash · Git

---

## Also built

- **Sensorway (internship)** — YOLOv8 defect detection for an IoT line, deployed on-site in Hungary.
- **Pancreas segmentation capstone** — CT and MRI segmentation for an external client, with a University of Sydney team. Private while in progress.
- **Startup** — grand prize at a Samsung enterprise competition, patent application filed.

---

<sub>If a number appears above, it came from a run I can point you at.</sub>
