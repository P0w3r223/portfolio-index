# Portfolio — Python · Data · AI

> **Telecommunications student building complete, data and AI projects in Python** —
> from data acquisition, through models, to deployed applications and their evaluation.
> Targeting AI Engineer and Data Scientist roles (open to Junior Python / ML Engineer).

This repository is the **index** of my portfolio, and it is **private**. The public landing
page is the profile README at [github.com/P0w3r223](https://github.com/P0w3r223), a separate
repository — said here because everything below reads as though it were addressed to a
recruiter, and a recruiter cannot open this page. It is for me, and for anyone I hand access to.

Each project below lives in its own repository with a dedicated README, tests, and (where
relevant) CI. The projects are ordered as a deliberate progression: each one adds a new layer
of skills and builds on the previous.

## Start here

- **AI Engineer** → **P5 · [doc-extract](https://github.com/P0w3r223/doc-extract)** — invoice extraction that knows when it is wrong · [**live site**](https://p0w3r223.github.io/doc-extract/)
- **Data Scientist** → **P2 · [ab-lab](https://github.com/P0w3r223/ab-lab)** — a 5% test is only 5% if you look once · [**live site**](https://p0w3r223.github.io/ab-lab/)

## Level A — data / AI projects

| # | Project | What it demonstrates | Status | Site |
|---|---------|----------------------|--------|------|
| A1 | [wroclaw-air-insights](https://github.com/P0w3r223/wroclaw-air-insights) | pandas, SQL, public APIs and a first scikit-learn model, built under time-series discipline: chronological splits and rolling-origin CV, every claim scored against two naive rules on the same folds and judged on the paired per-fold difference; a prediction interval ships only where its measured coverage held, and the constructions that missed are published as misses; and the forecast the page shows is logged before its hours exist and graded once they are — the one piece of evidence here fixed in advance of the outcome | ✅ Live | [🌐](https://p0w3r223.github.io/wroclaw-air-insights/) |
| A2 | [it-job-radar](https://github.com/P0w3r223/it-job-radar) | data engineering — one sitemap request observes the whole population, so presence is never sampled and only attributes cost a fetch; the unit of analysis is the *job*, not the advert (39 % of adverts are one role republished city by city, which had put azure third in the demand ranking instead of seventh); a figure known to be false is withheld and one measured imprecisely is greyed, by interval width as well as by `n`; versioned migrations, a normalization dictionary whose fixes reach stored data, and a contract enforced before publication; one SQL definition per metric, run in DuckDB over a redacted Parquet artifact and shown verbatim | ✅ Live | [🌐](https://p0w3r223.github.io/it-job-radar/) |
| A3 | [car-price-ml](https://github.com/P0w3r223/car-price-ml) | full ML cycle end-to-end — EDA, feature engineering, model comparison, FastAPI service with Docker; past that, what a valuation service does with input it cannot price: every categorical domain is closed, so an unseen make or a combustion car with no engine gets a 422 rather than a confident number; duplicates dropped before measurement (9.8 % of rows put identical cars in both CV folds); the served model chosen from a 16-configuration size↔quality curve — LightGBM at 8 612 ± 72 PLN MAE in 13.9 MB against RandomForest's 8 798 ± 81 in 590 MB; every price dated to the data it came from; and the valuation form runs that same model in the browser itself — dependency-free, no API and no framework, its vocabularies and bounds generated from the Python config, so without them it refuses to run rather than validating against a guess of its own | ✅ Live | [🌐](https://p0w3r223.github.io/car-price-ml/) · [🧮](https://p0w3r223.github.io/car-price-ml/app/) |

## Level B — supporting proofs

| # | Project | Skill proven | Site |
|---|---------|--------------|------|
| B1 | [mini-traceroute](https://github.com/P0w3r223/mini-traceroute) | C++ — traceroute on raw sockets (TTL, ICMP, CMake) | [🌐](https://p0w3r223.github.io/mini-traceroute/) |
| B2 | [auth-log-scan](https://github.com/P0w3r223/auth-log-scan) | Linux — SSH log parser with brute-force detection | [🌐](https://p0w3r223.github.io/auth-log-scan/) |
| B3 | [pl-review-sense](https://github.com/P0w3r223/pl-review-sense) | NLP in Polish — TF-IDF baseline vs. HerBERT transformer fine-tuning (Hugging Face) | [🌐](https://p0w3r223.github.io/pl-review-sense/) |
| B4 | [token-budget](https://github.com/P0w3r223/token-budget) | developer tooling — parse Claude Code transcripts, attribute token cost to milestones, enforce a budget (stdlib-only) | — |

## Level P — stage 2: engineering and methodology

Level A proved I can *build*. Stage 2 is about maintaining and measuring what I build —
targeting AI Engineer and Data Scientist roles.

| # | Project | What it demonstrates | Status | Site |
|---|---------|----------------------|--------|------|
| P1 | [mlops-car-price](https://github.com/P0w3r223/mlops-car-price) | MLOps on top of A3 — MLflow tracking and registry, drift monitoring whose detector is itself measured (false alarms, power), champion/challenger promotion decided by a paired bootstrap, API serving the champion alias | ✅ Live | [🌐](https://p0w3r223.github.io/mlops-car-price/) |
| P2 | [ab-lab](https://github.com/P0w3r223/ab-lab) | applied statistics — **a 5% test is only 5% if you look once, count each user once, and test one metric**: checked twenty times a true null is declared a winner 25.3% of the time, at twenty rows per user 44.0%, across twenty metrics 65.7%, and each is paired with the procedure that puts the rate back. Three independent routes to one conclusion, with the second and third derived on paper *before* the code existed so the simulation had something falsifiable to contradict. Underneath: power and sample size, Welch/proportion/Mann-Whitney/bootstrap, SRM, mSPRT, cluster-robust variance and multiplicity control — `statsmodels` only ever as a test oracle. The published page is generated from a committed record of counts, and a test fails if its bytes stop matching | ✅ Live | [🌐](https://p0w3r223.github.io/ab-lab/) |
| P3 | [apply-scout](https://github.com/P0w3r223/apply-scout) | an LLM agent written from scratch — tool loop, safety budgets, guardrails — and an evaluation that scores its own retriever and its own attack surface, offline from a committed recording | ✅ Live | [🌐](https://p0w3r223.github.io/apply-scout/) |
| P4 | [pl-jobs-lora](https://github.com/P0w3r223/pl-jobs-lora) | QLoRA fine-tuning of a small Polish LLM on a self-built dataset from A2, compared honestly against zero-shot and few-shot API baselines | 🚧 In progress | [🌐](https://p0w3r223.github.io/pl-jobs-lora/) |
| P5 | [doc-extract](https://github.com/P0w3r223/doc-extract) | structured extraction from Polish invoices where the point is not the extraction but the **error detection**: the Ministry's KSeF FA(3) schema is 183 798 bytes of XSD carrying 328 enumerations and **zero assertions**, so *net + VAT = gross* is unenforced by the national standard; 15 consistency rules fill that gap and are reported as data rather than raised, arithmetic identities counted apart from heuristics because a heuristic's false positives would otherwise be indistinguishable from a real miss; the corpus is generated so the gold needs no annotation step — KSeF-conformant XML *is* the ground truth, rendered to PDF across 9 difficulty tiers × 3 layouts and reproducible from one seed | 🚧 M6 of 7 done, M7 underway | [🌐](https://p0w3r223.github.io/doc-extract/) |

## Pinned on profile

Six slots, led by the AI Engineer flagship and the Data Scientist headline:

**P5 doc-extract** (extraction that knows when it is wrong) · **P2 ab-lab** (a 5% test is only 5% if you look once) · **P3 apply-scout** (agent, and an evaluation that scores its own retriever) · **P1 mlops-car-price** (MLOps) · **A1 wroclaw-air-insights** (data + forecast) · **A2 it-job-radar** (data engineering)

<sub>The pins are a GitHub **account setting**, not a file — nothing in this repository can read or
write them, so this list is a copy and the profile is the original. `A3 car-price-ml` was the slot
`doc-extract` took: the six were spending two of them on the same dataset. Reasoning in
[`docs/audit/0004_session1-recruiter-triage.md`](docs/audit/0004_session1-recruiter-triage.md) § 3.4.</sub>

## Conventions

- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/), work on branches + PRs with a "why" description.
- **Naming:** English repo names, descriptions, and tags.
- **Each project is defensible** in a technical interview — every non-trivial decision is documented.

---

<sub>Early Python practice scripts are preserved on the
[`archive/legacy-games`](https://github.com/P0w3r223/current_projects/tree/archive/legacy-games)
branch — kept for history, not part of the active portfolio.</sub>
