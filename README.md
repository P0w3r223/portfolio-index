# Portfolio — Python · Data · AI

> **Telecommunications student building complete, data and AI projects in Python** —
> from data acquisition, through models, to deployed applications and their evaluation.
> Targeting AI Engineer and Data Scientist roles (open to Junior Python / ML Engineer).

This repository is the **index** of my portfolio. Each project below lives in its own
repository with a dedicated README, tests, and (where relevant) CI. The projects are
ordered as a deliberate progression: each one adds a new layer of skills and builds on
the previous.

## ✅ Live now

- **A1 · [wroclaw-air-insights](https://github.com/P0w3r223/wroclaw-air-insights)** — Wrocław air quality analysis + 24h PM2.5 forecast · [**live site**](https://p0w3r223.github.io/wroclaw-air-insights/)
- **A2 · [it-job-radar](https://github.com/P0w3r223/it-job-radar)** — Polish IT job market: demand counted per *vacancy*, not per advert, and a data contract that refuses to publish figures failing it — one SQL definition per metric, shown verbatim beside its chart · [**live site**](https://p0w3r223.github.io/it-job-radar/)
- **A3 · [car-price-ml](https://github.com/P0w3r223/car-price-ml)** — used-car price model that refuses the cars it cannot price, runs in the reader's browser, and quotes the error measured for each price band · [**live site**](https://p0w3r223.github.io/car-price-ml/) · [**valuation form**](https://p0w3r223.github.io/car-price-ml/app/)
- **A4 · [pl-review-sense](https://github.com/P0w3r223/pl-review-sense)** — Polish review sentiment: TF-IDF vs HerBERT (PolEmo 2.0) · [**live site**](https://p0w3r223.github.io/pl-review-sense/)
- **A6 · [token-budget](https://github.com/P0w3r223/token-budget)** — developer tooling: track Claude Code token spend against a milestone budget (standard library only)
- **P2 · [ab-lab](https://github.com/P0w3r223/ab-lab)** — A/B experiment statistics: power, SRM, peeking correction — every method validated by simulation · [**live site**](https://p0w3r223.github.io/ab-lab/)
- **P1 · [mlops-car-price](https://github.com/P0w3r223/mlops-car-price)** — the A3 model kept alive: versioned data, MLflow registry, an *evaluated* drift detector, and promotion decided by a paired bootstrap · [**live site**](https://p0w3r223.github.io/mlops-car-price/)
- **P3 · [apply-scout](https://github.com/P0w3r223/apply-scout)** ⭐ — flagship LLM agent: a from-scratch tool loop with safety budgets, guardrails, and a trajectory-evaluation harness (success rate, citation fidelity, cost per task) · [**live site**](https://p0w3r223.github.io/apply-scout/)
- **P4 · [pl-jobs-lora](https://github.com/P0w3r223/pl-jobs-lora)** — QLoRA fine-tune of a small Polish LLM: prose → structured JSON, compared against API baselines (results pending the training run) · [**live site**](https://p0w3r223.github.io/pl-jobs-lora/)

## Level A — data / AI projects

| # | Project | What it demonstrates | Status | Site |
|---|---------|----------------------|--------|------|
| A1 | [wroclaw-air-insights](https://github.com/P0w3r223/wroclaw-air-insights) | pandas, SQL, visualization, working with APIs, first scikit-learn model with correct methodology (time-based split) | ✅ Live | [🌐](https://p0w3r223.github.io/wroclaw-air-insights/) |
| A2 | [it-job-radar](https://github.com/P0w3r223/it-job-radar) | data engineering — one sitemap request observes the whole population, so presence is never sampled and only attributes cost a fetch; the unit of analysis is the *job*, not the advert (39 % of adverts are one role republished city by city, which had put azure third in the demand ranking instead of seventh); a figure known to be false is withheld and one measured imprecisely is greyed, by interval width as well as by `n`; versioned migrations, a normalization dictionary whose fixes reach stored data, and a contract enforced before publication; one SQL definition per metric, run in DuckDB over a redacted Parquet artifact and shown verbatim | ✅ Live | [🌐](https://p0w3r223.github.io/it-job-radar/) |
| A3 | [car-price-ml](https://github.com/P0w3r223/car-price-ml) | full ML cycle end-to-end — EDA, feature engineering, model comparison, FastAPI service with Docker; past that, what a valuation service does with input it cannot price: every categorical domain is closed, so an unseen make or a combustion car with no engine gets a 422 rather than a confident number; duplicates dropped before measurement (9.8 % of rows put identical cars in both CV folds); the served model chosen from a 16-configuration size↔quality curve — LightGBM at 8 612 ± 72 PLN MAE in 14 MB against RandomForest's 8 798 ± 81 in 590 MB; every price dated to the data it came from | ✅ Live | [🌐](https://p0w3r223.github.io/car-price-ml/) · [🧮](https://p0w3r223.github.io/car-price-ml/app/) |
| A4 | [pl-review-sense](https://github.com/P0w3r223/pl-review-sense) | NLP in Polish — TF-IDF baseline vs. HerBERT transformer fine-tuning (Hugging Face) | ✅ Live | [🌐](https://p0w3r223.github.io/pl-review-sense/) |
| A5 | **studia-rag** | LLM/RAG app — embeddings, vector DB, source citation, retrieval evaluation | ⏸ Paused | — |
| A6 | [token-budget](https://github.com/P0w3r223/token-budget) | developer tooling — parse Claude Code transcripts, attribute token cost to milestones, enforce a budget (stdlib-only) | ✅ Live | — |

## Level B — supporting proofs

| # | Project | Skill proven |
|---|---------|--------------|
| B1 | [mini-traceroute](https://github.com/P0w3r223/mini-traceroute) ✅ | C++ — traceroute on raw sockets (TTL, ICMP, CMake) |
| B2 | [auth-log-scan](https://github.com/P0w3r223/auth-log-scan) ✅ | Linux — SSH log parser with brute-force detection |
| B3 | [car-price-ml frontend](https://p0w3r223.github.io/car-price-ml/app/) ✅ | JavaScript — dependency-free valuation form that runs the trained model itself, with no API and no framework. Its vocabularies and bounds are generated from the Python config; without them it refuses to run rather than validating against a guess of its own |

## Level P — stage 2: engineering and methodology

Level A proved I can *build*. Stage 2 is about maintaining and measuring what I build —
targeting AI Engineer and Data Scientist roles.

| # | Project | What it demonstrates | Status | Site |
|---|---------|----------------------|--------|------|
| P1 | [mlops-car-price](https://github.com/P0w3r223/mlops-car-price) | MLOps on top of A3 — MLflow tracking and registry, drift monitoring whose detector is itself measured (false alarms, power), champion/challenger promotion decided by a paired bootstrap, API serving the champion alias | ✅ Live | [🌐](https://p0w3r223.github.io/mlops-car-price/) |
| P2 | [ab-lab](https://github.com/P0w3r223/ab-lab) | applied statistics — power and sample size, Welch/proportion/Mann-Whitney/bootstrap, SRM, mSPRT sequential testing; every method validated on thousands of simulated experiments | ✅ Live | [🌐](https://p0w3r223.github.io/ab-lab/) |
| P3 | [apply-scout](https://github.com/P0w3r223/apply-scout) ⭐ | flagship — an LLM agent written from scratch (tool loop, budgets, guardrails) with a trajectory-evaluation harness: success rate, citation fidelity, cost per task | ✅ Live | [🌐](https://p0w3r223.github.io/apply-scout/) |
| P4 | [pl-jobs-lora](https://github.com/P0w3r223/pl-jobs-lora) | QLoRA fine-tuning of a small Polish LLM on a self-built dataset from A2, compared honestly against zero-shot and few-shot API baselines | 🚧 In progress | [🌐](https://p0w3r223.github.io/pl-jobs-lora/) |
| P5 | **doc-extract** | structured extraction from Polish invoices — LLM structured outputs, Pydantic domain validation, per-field accuracy | 📋 Optional | — |

## Pinned on profile

⭐ **P3 apply-scout** (flagship agent) · **P1 mlops-car-price** (MLOps) · **P2 ab-lab** (applied statistics) · **A3 car-price-ml** (full ML cycle) · **A1 wroclaw-air-insights** (data + forecast) · **A2 it-job-radar** (data engineering)

## Conventions

- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/), work on branches + PRs with a "why" description.
- **Naming:** English repo names, descriptions, and tags.
- **Each project is defensible** in a technical interview — every non-trivial decision is documented.

---

<sub>Early Python practice scripts are preserved on the
[`archive/legacy-games`](https://github.com/P0w3r223/current_projects/tree/archive/legacy-games)
branch — kept for history, not part of the active portfolio.</sub>
