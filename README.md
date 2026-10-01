# Edward Hwang

I build full-stack products, backend systems, and machine-learning research tools, with an emphasis on testable behaviour and clear evaluation.

Studying Computer Science at the University of Sydney · Sydney, Australia  
Open to 2027 graduate and junior roles in software engineering, backend, and applied ML.

**[Portfolio](https://edwards-world.vercel.app/?view=index)** · [Explore Edward's World](https://edwards-world.vercel.app) · [LinkedIn](https://linkedin.com/in/soon-hyun-hwang-7212a42b7) · [Email](mailto:edwardhwang1223@gmail.com)

## Selected projects

### [SportsGang / Protin](https://github.com/EdwardH-jedi/Sportsgang)

A mobile app for discovering sports partners, matching and chatting, arranging sports sessions, and tracking results.

**Stack:** React Native / Expo · TypeScript · FastAPI · PostgreSQL · Redis · Docker

- **Engineering focus:** async backend services, an explicit booking state machine, database migrations, a notification worker, and shared mobile/API contracts
- **Release:** SportsGang v1.0 passed Apple App Review on 13 May 2026. The public App Store listing is linked below; release approval is separate from current backend availability
- **Evidence:** the repository documents the release process and separates API unit tests, mobile tests, and PostgreSQL/Redis integration checks

<p>
  <img src="https://raw.githubusercontent.com/EdwardH-jedi/Sportsgang/main/docs/release/screenshots/ios/01-discovery-gym-partners.png" width="30%" alt="SportsGang opponent discovery screen">
  <img src="https://raw.githubusercontent.com/EdwardH-jedi/Sportsgang/main/docs/release/screenshots/ios/03-chat-confirmed-session.png" width="30%" alt="SportsGang confirmed-session chat screen">
  <img src="https://raw.githubusercontent.com/EdwardH-jedi/Sportsgang/main/docs/release/screenshots/ios/05-propose-session-form.png" width="30%" alt="SportsGang session proposal screen">
</p>

[Source](https://github.com/EdwardH-jedi/Sportsgang) · [App Store](https://apps.apple.com/us/app/sportsgang/id6767027447) · [Release evidence](https://github.com/EdwardH-jedi/Sportsgang/blob/main/docs/PORTFOLIO_FACTS.md) · [Verification scope](https://github.com/EdwardH-jedi/Sportsgang/blob/main/docs/VERIFICATION.md)

### [AFL Predict](https://github.com/EdwardH-jedi/AFL_predict)

An AFL match-prediction research system covering data ingestion, temporal features, calibrated models, walk-forward evaluation, and paper-trading analytics.

**Stack:** Python · XGBoost · scikit-learn · FastAPI · SQLAlchemy

- **Engineering focus:** leakage controls, reproducible evaluation, pipeline orchestration, database migrations, and explicit readiness checks
- **Scope:** paper-trading research only, with no live betting. The repository makes no supported claim that its models outperform bookmaker prices
- **Evaluation limits:** historical results require external data to reproduce, and the calibrated ensemble used for recommendations has not been evaluated by the backtest runner

[Source](https://github.com/EdwardH-jedi/AFL_predict) · [Evaluation evidence and limits](https://github.com/EdwardH-jedi/AFL_predict/blob/main/docs/PORTFOLIO_FACTS.md) · [Backtesting method](https://github.com/EdwardH-jedi/AFL_predict/blob/main/docs/backtesting.md)

### [Edward's World](https://github.com/EdwardH-jedi/Edward_world)

An interactive portfolio built as a pixel town, with four project experiences and a personal room. **VIEW PROJECTS** opens a reading view directly from the title screen.

**Stack:** Next.js 16 · React · TypeScript · Canvas 2D · anime.js · Vitest

- **Engineering focus:** procedural art, pure game simulations, separate state and animation layers, browser persistence, and keyboard/touch controls
- **Scope:** the project experiences are portfolio recreations; their case studies link to the original products and explain the differences
- **Verification:** a dated deployment report records automated checks and browser testing, including the configuration-dependent golf board

[Live portfolio](https://edwards-world.vercel.app) · [Project index](https://edwards-world.vercel.app/?view=index) · [Source](https://github.com/EdwardH-jedi/Edward_world) · [Architecture](https://github.com/EdwardH-jedi/Edward_world/blob/main/docs/ARCHITECTURE.md) · [Case study](https://github.com/EdwardH-jedi/Edward_world/blob/main/docs/CASE_STUDY.md) · [Recorded verification](https://github.com/EdwardH-jedi/Edward_world/blob/main/docs/predeploy/FINAL_PRODUCTION_DEPLOY.md)

### [Wardrobe](https://github.com/EdwardH-jedi/wardrobe)

A local-first fashion archive for saving garment photos, editing metadata, composing outfits, and keeping looks in the browser.

**Stack:** React · TypeScript · Vite · IndexedDB; optional Three.js / FastAPI experiments

- **Engineering focus:** hydration and persistence fallbacks, image-asset storage, and layered outfit composition
- **Scope:** the default archive works without a backend. Its styling preview is 2.5D, and the separate proxy-3D track is experimental; it does not provide real virtual try-on or sizing

[Source](https://github.com/EdwardH-jedi/wardrobe) · [Architecture](https://github.com/EdwardH-jedi/wardrobe/blob/main/docs/ARCHITECTURE.md) · [Feature scope](https://github.com/EdwardH-jedi/wardrobe/blob/main/docs/PROJECT_SCOPE.md)

## More work

- **[Career Quest / SoonPerMario](https://github.com/EdwardH-jedi/career-quest):** a playable résumé built with HTML5 Canvas and vanilla JavaScript, with no build step
- **Pancreas segmentation capstone:** ML training and experiments for multi-centre medical-image segmentation; the university project remains private while in progress
- **Sensorway:** worked on a YOLOv8 defect-detection and monitoring system for an IoT production line, including an on-site deployment in Hungary
- **Samsung enterprise competition:** grand prize; patent application filed by the team

## Technical focus

- **Product engineering:** React, TypeScript, React Native / Expo, Next.js, Vite, SwiftUI
- **Backend and data:** Python, FastAPI, PostgreSQL, SQLAlchemy, Redis, Docker
- **ML and computer vision:** PyTorch, MONAI, XGBoost, SHAP, YOLO, evaluation pipelines
- **Systems and tooling:** C, Linux, bash, Git, CI, automated testing

## How I work

I use coding agents for implementation support and independent review. I set the scope, architecture, acceptance criteria, and verification approach, and review the results before accepting changes. The project links above include source code, release records, and evaluation limits so that the work can be inspected beyond a demo.
