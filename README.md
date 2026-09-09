# Edward Hwang

**Software engineer building full-stack products, backend systems, and evaluation-first machine learning.**

Final-year Computer Science student at the University of Sydney · Sydney, Australia · Graduating December 2026  
Open to 2027 graduate and junior roles in software engineering, backend, and applied ML.

**[Explore Edward's World →](https://edwards-world.vercel.app)** · [LinkedIn](https://linkedin.com/in/soon-hyun-hwang-7212a42b7) · [Email](mailto:edwardhwang1223@gmail.com)

---

## Featured work

### [Edward's World](https://github.com/EdwardH-jedi/Edward_world) — interactive developer portfolio

`Next.js 16` · `TypeScript` · `Canvas 2D` · `Vitest`

Portfolio projects rebuilt as places you can walk into and use: a sports matchmaking product, an ML research lab, a local-first wardrobe, and a playable résumé inside one procedural pixel world. A plain accessible index provides a fast path for reviewers who would rather read than explore.

**Shipped:** live on Vercel · five complete experiences · keyboard and touch support · reduced-motion support · 391 tests across 29 files

[Live demo](https://edwards-world.vercel.app) · [Source](https://github.com/EdwardH-jedi/Edward_world) · [Case study](https://github.com/EdwardH-jedi/Edward_world/blob/main/docs/CASE_STUDY.md) · [Architecture](https://github.com/EdwardH-jedi/Edward_world/blob/main/docs/ARCHITECTURE.md)

---

### [Protin / SportsGang](https://github.com/EdwardH-jedi/Sportsgang) — full-stack mobile sports matchmaking

`React Native / Expo` · `FastAPI` · `PostgreSQL` · `Redis` · `Docker`

A mobile product for finding sports partners, matching and messaging, proposing sessions, booking venues, recording results, and maintaining rankings. The backend uses an async service layer, explicit booking state transitions, migrations, background workers, and typed mobile contracts.

**Shipped:** SportsGang v1.0 approved by App Store review on 13 May 2026 · 620 API tests · 747 mobile tests

<p>
  <img src="https://raw.githubusercontent.com/EdwardH-jedi/Sportsgang/main/docs/release/screenshots/ios/01-discovery-gym-partners.png" width="30%" alt="SportsGang opponent discovery screen">
  <img src="https://raw.githubusercontent.com/EdwardH-jedi/Sportsgang/main/docs/release/screenshots/ios/03-chat-confirmed-session.png" width="30%" alt="SportsGang confirmed-session chat screen">
  <img src="https://raw.githubusercontent.com/EdwardH-jedi/Sportsgang/main/docs/release/screenshots/ios/05-propose-session-form.png" width="30%" alt="SportsGang session proposal screen">
</p>

[Source](https://github.com/EdwardH-jedi/Sportsgang) · [Release evidence](https://github.com/EdwardH-jedi/Sportsgang/blob/main/docs/PORTFOLIO_FACTS.md) · [Verification scope](https://github.com/EdwardH-jedi/Sportsgang/blob/main/docs/VERIFICATION.md)

---

### [AFL Predict](https://github.com/EdwardH-jedi/AFL_predict) — evaluation-first sports ML system

`Python` · `XGBoost` · `scikit-learn` · `FastAPI` · `SQLAlchemy`

A research system for AFL head-to-head prediction with scheduled ingestion, temporal feature engineering, calibrated ensembles, walk-forward evaluation, paper-trading analytics, and explicit readiness gates. The project prioritises leakage controls and reproducible evaluation over headline accuracy.

**Verified:** 313 tests passing · fresh-database migration chain checked · daily pipeline and readiness gate run end to end  
**Research status:** preliminary; no claim that the models outperform bookmaker prices

[Source](https://github.com/EdwardH-jedi/AFL_predict) · [Evaluation evidence](https://github.com/EdwardH-jedi/AFL_predict/blob/main/docs/PORTFOLIO_FACTS.md) · [Backtesting method](https://github.com/EdwardH-jedi/AFL_predict/blob/main/docs/backtesting.md)

---

### [Wardrobe](https://github.com/EdwardH-jedi/wadrobe) — local-first fashion archive

`React` · `TypeScript` · `IndexedDB` · `Three.js` · `FastAPI`

A browser-first wardrobe for recording garments, editing metadata, composing outfits, and saving looks locally. Image preparation, optional vision integrations, and an experimental proxy-3D path are isolated from the default archive so the core product remains usable without cloud services.

**Built:** persistent local archive with fallbacks · layered outfit composition · saved looks · optional image analysis · scoped GLB preview experiment

[Source](https://github.com/EdwardH-jedi/wadrobe) · [Architecture](https://github.com/EdwardH-jedi/wadrobe/blob/main/docs/ARCHITECTURE.md) · [Feature scope](https://github.com/EdwardH-jedi/wadrobe/blob/main/docs/PROJECT_SCOPE.md)

---

## More work

**[SoonPerMario](https://github.com/EdwardH-jedi/soonpermario)** — a playable résumé built as an HTML5 Canvas platformer with vanilla JavaScript.  
**Pancreas segmentation capstone** — ML training and experiments for multi-centre medical-image segmentation; private while the university project is in progress.

## Technical focus

**Product engineering** — React, TypeScript, React Native / Expo, Next.js, Vite, SwiftUI  
**Backend and data** — Python, FastAPI, PostgreSQL, SQLAlchemy, Redis, Docker  
**ML and computer vision** — PyTorch, MONAI, XGBoost, SHAP, YOLO, evaluation pipelines  
**Systems and tooling** — C, Linux, bash, Git, CI, automated testing

## Beyond public repositories

**Sensorway** — worked on a YOLOv8 defect-detection and monitoring system for an IoT production line, including an on-site deployment in Hungary.  
**Samsung enterprise competition** — grand prize; patent application filed by the team.

## Engineering approach

I use coding agents for implementation support and independent review, but scope, architecture, acceptance criteria, testing, benchmarks, and final judgement remain human-directed. The output is not accepted because a model produced it; it stays only when the product and evidence hold up.
