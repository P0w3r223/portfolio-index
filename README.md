# Portfolio — Python · Data · AI

> **Telecommunications student building complete data/AI projects in Python** —
> from data acquisition, through models, to deployed applications.
> Targeting Junior Python Developer / Junior Data Analyst / Junior ML Engineer roles.

This repository is the **index** of my portfolio. Each project below lives in its own
repository with a dedicated README, tests, and (where relevant) CI. The projects are
ordered as a deliberate progression: each one adds a new layer of skills and builds on
the previous.

## ✅ Live now

- **A1 · [wroclaw-air-insights](https://github.com/P0w3r223/wroclaw-air-insights)** — Wrocław air quality analysis + 24h PM2.5 forecast · [**live site**](https://p0w3r223.github.io/wroclaw-air-insights/)
- **A2 · [it-job-radar](https://github.com/P0w3r223/it-job-radar)** — Polish IT job market: tech trends & salary ranges · [**live site**](https://p0w3r223.github.io/it-job-radar/)
- **A3 · [car-price-ml](https://github.com/P0w3r223/car-price-ml)** — used-car price model: bake-off, SHAP, FastAPI + Docker · [**live site**](https://p0w3r223.github.io/car-price-ml/)
- **A4 · [pl-review-sense](https://github.com/P0w3r223/pl-review-sense)** — Polish review sentiment: TF-IDF vs HerBERT (PolEmo 2.0) · [**live site**](https://p0w3r223.github.io/pl-review-sense/)
- **A6 · [token-budget](https://github.com/P0w3r223/token-budget)** — developer tooling: track Claude Code token spend against a milestone budget (standard library only)
- **P2 · [ab-lab](https://github.com/P0w3r223/ab-lab)** — A/B experiment statistics: power, SRM, peeking correction — every method validated by simulation

🚧 Next: **P1 mlops-car-price** (model in production) and the flagship **P3 apply-scout** (LLM agent with trajectory evaluation).

## Level A — data / AI projects

| # | Project | What it demonstrates | Status | Site |
|---|---------|----------------------|--------|------|
| A1 | [wroclaw-air-insights](https://github.com/P0w3r223/wroclaw-air-insights) | pandas, SQL, visualization, working with APIs, first scikit-learn model with correct methodology (time-based split) | ✅ Live | [🌐](https://p0w3r223.github.io/wroclaw-air-insights/) |
| A2 | [it-job-radar](https://github.com/P0w3r223/it-job-radar) | data engineering — collecting IT job offers, schema design, aggregating SQL, normalization, respectful scraping | ✅ Live | [🌐](https://p0w3r223.github.io/it-job-radar/) |
| A3 | [car-price-ml](https://github.com/P0w3r223/car-price-ml) | full ML cycle end-to-end — EDA, feature engineering, model comparison, FastAPI prediction API with Docker | ✅ Live | [🌐](https://p0w3r223.github.io/car-price-ml/) |
| A4 | [pl-review-sense](https://github.com/P0w3r223/pl-review-sense) | NLP in Polish — TF-IDF baseline vs. HerBERT transformer fine-tuning (Hugging Face) | ✅ Live | [🌐](https://p0w3r223.github.io/pl-review-sense/) |
| A5 | **studia-rag** | LLM/RAG app — embeddings, vector DB, source citation, retrieval evaluation | ⏸ Paused | — |
| A6 | [token-budget](https://github.com/P0w3r223/token-budget) | developer tooling — parse Claude Code transcripts, attribute token cost to milestones, enforce a budget (stdlib-only) | ✅ Live | — |

## Level B — supporting proofs (one weekend each)

| # | Project | Skill proven |
|---|---------|--------------|
| B1 | [mini-traceroute](https://github.com/P0w3r223/mini-traceroute) ✅ | C++ — traceroute on raw sockets (TTL, ICMP, CMake) |
| B2 | [auth-log-scan](https://github.com/P0w3r223/auth-log-scan) ✅ | Linux — SSH log parser with brute-force detection |
| B3 | car-price-ml frontend | JavaScript — car-price form (vanilla JS + fetch to the A3 API) |

## Level P — stage 2: engineering and methodology

Level A proved I can *build*. Stage 2 is about maintaining and measuring what I build —
targeting AI Engineer and Data Scientist roles.

| # | Project | What it demonstrates | Status |
|---|---------|----------------------|--------|
| P1 | **mlops-car-price** | MLOps on top of A3 — MLflow tracking and model registry, data drift monitoring, champion/challenger retraining, versioned API | 📋 Planned |
| P2 | [ab-lab](https://github.com/P0w3r223/ab-lab) | applied statistics — power and sample size, Welch/proportion/Mann-Whitney/bootstrap, SRM, mSPRT sequential testing; every method validated on thousands of simulated experiments | ✅ Live |
| P3 | **apply-scout** ⭐ | flagship — an LLM agent written from scratch (tool loop, budgets, guardrails) with a trajectory-evaluation harness: success rate, citation fidelity, cost per task | 📋 Planned |
| P4 | **pl-jobs-lora** | QLoRA fine-tuning of a small Polish LLM on a self-built dataset from A2, compared honestly against zero-shot and few-shot API baselines | 📋 Planned |
| P5 | **doc-extract** | structured extraction from Polish invoices — LLM structured outputs, Pydantic domain validation, per-field accuracy | 📋 Optional |

## Pinned on profile

⭐ **P3 apply-scout** (flagship agent) · **P1 mlops-car-price** (model in production) · **A3 car-price-ml** (full ML cycle)

## Conventions

- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/), work on branches + PRs with a "why" description.
- **Naming:** English repo names, descriptions, and tags.
- **Each project is defensible** in a technical interview — every non-trivial decision is documented.

---

<sub>Early Python practice scripts are preserved on the
[`archive/legacy-games`](https://github.com/P0w3r223/current_projects/tree/archive/legacy-games)
branch — kept for history, not part of the active portfolio.</sub>
