# Session 2 — Extensions

Date: 2026-09-03. **Reconciled 2026-09-04** against the repositories: four of the five items § 9
carried as open had landed or been decided, and none of them said so — see the section at the foot of
§ 9 and `0003` § 11.
Status: accepted — all three decisions in § 9 taken 2026-09-03 and executed by 2026-09-04
Author: P0w3r223
Related to: [0003_portfolio-review-plan.md](0003_portfolio-review-plan.md) § 3 (the commission) and § 9 (the reconciliation rule), [0004_session1-recruiter-triage.md](0004_session1-recruiter-triage.md) § 5, § 7 and § 8

---

## 1. What this session had to answer

`0003` § 3 commissions it in one line: *for each limiting project — extend / repackage / remove,
with cost and payoff, inside the 1–2 month budget.* The output is prioritised proposals, not
merged work.

It inherits four named items from `0004` § 8:

- the **RAG / retrieval-evaluation gap**, the one hole in the stack;
- `apply-scout`'s **security debt**, deferred here rather than into a presentation pass because
  *naming it in the README is the minimum and confining the loop is the real fix*;
- `doc-extract`'s **zero topics** and `car-price-ml`'s **reported language** — both closed ahead of
  this document, see § 2.1;
- and, from the same triage, the two projects demoted to Level B: **`token-budget`** and
  **`pl-review-sense`**.

The budget is the plan's own: **1–2 months**, `0003` § 4. Every estimate below is in focused
working days against that ceiling, and each one names what drives it.

## 2. Method

Every claim in § 3–§ 7 was read out of the repository, not out of an earlier document — the rule
`0003` § 9 exists to enforce. Where a number appears it is measured and the measurement is stated
beside it, so a later session can re-run it rather than trust it.

Costs are estimates and are marked as such. They are ranges because the thing that moves them is
named in each case; a single number would be a false precision this portfolio's own argument
rejects.

### 2.1 Three items closed before the session opened

Carried out first because each was cheap, unambiguous and already decided:

- **`doc-extract`: 0 → 13 topics.** It was the only repository in the portfolio with none, against
  6–14 on its siblings, and it is the AI Engineer flagship — so the one project a topic search
  could not reach was the one the portfolio most wants found. `ocr` was deliberately **not** among
  them: there is no OCR engine here, `degrade/page.py` *simulates* what one would emit and the
  reading is done by a vision model, so the topic would assert something the repository does not
  contain.
- **`auth-log-scan`: `homepage` set.** It serves a live page (HTTP 200) and its repository card
  linked nowhere. All twelve are now consistent: eleven with a page carry the URL, `token-budget`
  is empty and correctly so — it has no page, which is the fact that demoted it.
- **`car-price-ml`: the reported language** — `car-price-ml#21`, green, awaiting merge.
  `Jupyter Notebook: 259433` from the languages API equals the single notebook's blob size **to the
  byte**, so one file outweighed `src/`, `api/`, the site builder and the tests together. One line
  of `.gitattributes` (`notebooks/*.ipynb linguist-documentation`), which is a rule that file
  already states one line above for `model.json` — *"would otherwise make this a JSON project"*.

## 3. What the survey found before any proposal was written

Two findings that change what the proposals should say. Both were arrived at by reading source
that the earlier sessions had described from the outside.

### 3.1 `apply-scout` already contains a retrieval evaluation — and it cannot see its own retriever

The gap `0004` § 7 names is *RAG and retrieval evaluation*. Three quarters of that machinery is
already in `apply-scout`, and has been since milestone 3:

| piece | where | what it is |
|---|---|---|
| the corpus | `github.py` | the candidate's repositories + READMEs, paginated, cached on disk |
| the retriever | `tools/github_evidence.py` → `find_evidence()` | pure function: requirement + repos + READMEs → `Evidence[]` |
| the generator | `synthesis.py` | report + cover letter, citing the retrieved evidence |
| the grounding metrics | `guardrail.py` → `evidence_grounding()`, `requirement_grounding()` | do the citations trace to what was actually retrieved and fetched |
| the offline harness | `cassette.py`, `evaluation.py` | every external seam recorded; CI replays the tables byte-identical, $0 |

**What is missing is the retrieval half, and its absence is structural rather than an oversight.**
`evidence_grounding(report, retrieved)` scores the report's links *against what the retriever
returned* — so **the retrieval is the ground truth**. If `find_evidence` misses the repository that
proves a requirement, nothing in the harness notices: the report cannot cite what it was never
given, and a report citing nothing scores `n/a`, not zero.

> **Corrected the same day, before any of this was acted on.** The paragraph below originally
> presented the retriever's weakness as something nobody had noticed. That is wrong, and the source
> of the error is the one this review keeps naming: I read the code and not the project's own
> account of itself. `apply-scout`'s README names it as limitation **#3 of 18**, calls it *"the
> bigger miss"*, and **measures it** — *63 of 72 probes (87 %) return no evidence, and 48 of those 63
> contain a distinctive keyword that **is** present in one of the READMEs* (`qlora`, `mlflow`,
> `langchain`, `transformer`, `guardrails`, `docker`, `sentiment` among them). It even explains why
> it was not fixed: a sharper probe changes what the tool returns, which changes the conversation
> every cassette entry is keyed on, so it costs a full paid re-record.
>
> **What survives the correction is sharper than what it replaces.** The project has *measured* its
> retrieval defect and put the number **in prose only** — it is in no metric, no table, no test and
> no CI check. So the harness cannot see it, cannot score it, and cannot fail on a regression of it,
> while scoring five other things to three decimal places. And the 48-of-63 keyword analysis is
> already most of a relevance judgment set, which makes § 4's variant B cheaper rather than
> redundant. The three statements below were re-checked against the README after the correction and
> none of them is named there.

That matters because the retriever is weaker than the rest of the project. Of the three below, the
first is the one the README names and measures; the second and third are not in the limitations list
at all:

- **It matches the whole requirement string as one literal substring** — `needle in
  readme.text.lower()` (`github_evidence.py:46`), where `needle` is the requirement lowercased and
  stripped. A requirement phrased *"experience with retrieval-augmented generation"* matches only a
  README containing that exact sentence. **This one the README names and measures** (87 % of probes
  return nothing; three quarters of those misses are recoverable) — and the measurement lives in
  prose, not in the harness.
- **It does not rank.** Everything that matched is returned in repository-list order. There is no
  score, no top-*k*, and therefore nothing that recall@*k* or MRR could be computed over today.
- **The portfolio's better matcher is not wired to it.** `matching.tokens()` / `mentions()` — the
  containment matcher that was fixed in milestone 17 for shattering Polish words — is used by the
  **guardrail and the eval harness**, not by the retriever. The smarter function scores the output;
  the blunter one finds the evidence.

So the honest statement is not *"the portfolio has no RAG"*, and — after the correction above — it
is not *"nobody noticed the retriever"* either. It is: **the portfolio has a retrieval-augmented
pipeline whose retrieval step is the only link in the chain that is diagnosed in prose and scored by
nothing.** Every other link has a column in a published table and a test that can redden. This one
has a paragraph.

That reframes the gap from *build something new* to *finish something already three quarters built*
— and it is what makes variant B in § 4 cheap.

### 3.2 `pl-review-sense` was demoted on its headline, and the repository is larger than the headline

`0004` § 5 records the reason: *"TF-IDF against HerBERT on PolEmo 2.0 is a textbook exercise. Done
properly, but it distinguishes nothing."* Session 1 flagged its own uncertainty in the next
paragraph — *"The demotion is a presentation judgment, not a claim that the work is weak."* Read
against the repository, that caveat is carrying more weight than it looks.

What is actually in there: **5 607 lines of Python, 14 test files, 40 commits**, and modules the
one-line description does not imply —

- `stats.py` — bootstrap confidence intervals, and a **paired McNemar test** on the reviews the two
  models disagree on, rather than two accuracies printed side by side;
- `challenge.py` + `challenge_set.py` + `docs/adr/0002_challenge-set-design.md` — an **80-sentence
  Polish challenge set written for this project**: negation, irony, contrastive pivots, a control
  cell, plus variants with diacritics stripped and typos introduced;
- `cascade.py` — the **cost** of routing the least-confident share to the transformer, so the GPU
  bill is a fraction of traffic rather than all of it;
- `curves.py` — a learning curve separating what the corpus contributes from what the model does;
- `interpret.py` — the heaviest coefficients per class.

And the presentation inversion `0004` § 3.2 identified applies here in the demoted project's
favour: its live page opens

> `<h1>HerBERT reaches 0.986 against the baseline's 0.944</h1>`

— a **claim as the title**, the family A pattern Session 1 named as the good one — while
`apply-scout`, `mlops-car-price` and `pl-jobs-lora`, three Level A projects, still open with a
repository name.

**This does not automatically reverse the demotion.** The ranking question is *what sixty seconds
buys a reader*, and "sentiment classification on a public Polish benchmark" is a weaker opening
than "an agent with an evaluation harness" whatever is underneath it. What it does establish is
that **the recorded reason describes the project's title and not its contents**, and a reason that
does not describe the thing it justifies will not survive the next reader who opens the repository.
§ 7 puts the options.

## 4. The RAG gap — three variants, costed

Scope constraint inherited from `0004` § 7 and unchanged: **retrieval evaluation, not a chat UI.**
A chat UI measures nothing, and the portfolio's whole argument is that things are measured.

### Variant A — a new repository, retrieval evaluation from scratch

A thirteenth project: a corpus, a query set with relevance judgments, at least two retrievers
(lexical and dense) compared on recall@*k* / MRR / nDCG@10 with bootstrap intervals, its own page
and CI.

| | |
|---|---|
| **Cost** | **12–18 days** |
| corpus selection, licensing, ingestion | 2–3 d |
| **relevance judgments** | **3–5 d** — the item that dominates, unless a benchmark that ships them is reused, in which case 1 d and the project's own contribution shrinks accordingly |
| two retrievers (BM25 + dense) | 2–3 d |
| metrics, intervals, tests, CI | 3–4 d |
| page, README, ADRs | 2–3 d |
| **Payoff** | The gap is closed *in the name*. Discoverable by topic and by repository title, own card, own page, unambiguous to a recruiter scanning a list |
| **Risk** | A thirteenth surface to maintain, in a portfolio that has just spent three sessions *reducing* surfaces and their divergence. Hand-made relevance judgments are also the weakest kind of "measured" claim here — nothing external validates them, which is the opposite of how `ab-lab` and `doc-extract` earn their standing |

### Variant B — measure `apply-scout`'s retriever, and fix what the measurement finds

Turn the chain in § 3.1 into a measured one: annotate relevance judgments over the **existing**
8-posting cassette, give `find_evidence` a ranking, and compare retrievers — exact substring (today)
vs `matching.tokens` containment vs embeddings — on retrieval metrics, entirely offline.

| | |
|---|---|
| **Cost** | **4–7 days** — revised down from 5–8 by § 3.1's correction, which found the annotation half already largely done |
| relevance judgments over the recorded corpus | **1 d** — revised down after § 3.1's correction. The corpus, the postings and the requirement lists are already recorded and committed, **and the README's 48-of-63 keyword analysis is most of a judgment set already**: it names, per missed probe, the README that should have matched |
| ranking + top-*k* in `find_evidence`, behind the existing pure-function seam | 1–2 d |
| retrieval metrics (recall@*k*, MRR, nDCG) beside the existing eval table | 1–2 d |
| a second and third retriever to compare against | 1–2 d |
| ADR + README + page | 1 d |
| **Payoff** | Closes the gap **and** turns the project's own prose diagnosis into a scored one. After § 3.1's correction this is the sharper claim: `apply-scout` has *already found* its retrieval defect and quantified it at 87 %, and that number sits in a README bullet where nothing can regress on it, beside five other properties scored to three decimals in a published table. Variant B moves it into the table, which is the difference between a project that knows its weakness and one that measures it. Runs at **$0** — the cassette replays with no network and no key, machinery this project already has and a new repository would have to build. Also repairs `apply-scout`'s standing: `0004` kept it and took its ⭐ partly because *the presentation is the worst in the portfolio* |
| **Risk** | **Discoverability.** A recruiter searching "RAG" or "retrieval" does not find a repository called `apply-scout` unless the topics, the description and the page `h1` say so. That is a real objection and a cheap one to answer — § 2.1 has just demonstrated that topics cost minutes |

### Variant C — retrieval over `doc-extract`'s corpora

`doc-extract` has five corpora, span-level grounding (`ground/resolve.py`, `place.py`, `joint.py`,
`complete.py`) and 25 628 lines of Python. Retrieval over those documents would be technically at
home.

| | |
|---|---|
| **Cost** | **8–12 days** — the corpora exist, but nothing about invoice extraction currently poses a *retrieval* question, so the query set and its judgments are built from nothing |
| **Payoff** | Strengthens the flagship, and the grounding layer is genuinely adjacent work |
| **Risk** | **Highest conceptual cost.** This project's thesis is one sentence — *invoice extraction that knows when it is wrong* — and it is the sharpest thesis in the portfolio. Bolting a second question onto it dilutes the asset that won it the flagship position, to close a gap that has a cheaper host |

### Recommendation

**Variant B**, with the discoverability objection answered explicitly as part of it (topics,
repository description, and the page `h1` — which family B needs rewritten in Session 4 anyway).

The reasoning is the portfolio's own: a measured negative result about a component that was
believed adequate is worth more here than a new project asserting a capability. Variant B produces
exactly that shape of result, and § 3.1 already predicts what it will find. Variant A is the
honest fallback if the judgment is that a recruiter must see the word in a repository name.

## 5. `apply-scout`'s security debt

### What is actually there

Three legs, each verified in source rather than inferred:

1. **Arbitrary file read.** `tools/read_cv.py:47` — `path = Path(data.path)`. No base-directory
   join, no `resolve()`, no containment check. The path is an argument **the model chooses**, and
   the file's contents are returned to the model.
2. **SSRF.** `fetch.py:70–74` — `httpx.Client(follow_redirects=True)`. No scheme check, no host
   allowlist, no loopback or link-local guard, and redirects are followed without re-checking each
   hop. The URL is likewise **model-chosen**. The only filter is a content-type test *after* the
   request has already been made.
3. **The return path.** Fetched page text goes back into the conversation, so an untrusted document
   is read by the model as instructions unless something separates data from instruction — and
   nothing does.

**And the README does not name any of it.** Its limitations list runs to **eighteen** items; the
words `injection`, `untrusted`, `SSRF`, `allowlist` and `path traversal` appear in neither the
README nor `CLAUDE.md`.

This is the exact weakness `doc-extract` was promoted over — `0004` § 5 gave that as the deciding
reason, and it is the more uncomfortable finding of the two because `apply-scout` is the project
the portfolio has pointed at for longest.

### Three levels

| | scope | cost | what it leaves |
|---|---|---|---|
| **B1 — name it** | Add the three legs to the README's limitations and to `CLAUDE.md` | **0.5 d** | Honest, and the loop is still open. Acceptable only as a same-day stopgap while B2 lands |
| **B2 — confine the loop** | `read_cv`: join against a declared base directory, `resolve()`, refuse anything outside it. `fetch`: scheme allowlist, resolve the host and reject private / loopback / link-local ranges, cap and re-check every redirect hop. Tests for each refusal | **3–4 d** | The real fix. But the project's argument is that things are *measured*, and this would be the one safety property in it asserted rather than scored |
| **B3 — confine and measure** | B2, plus an attack suite scoring **attack success rate before and after**, modelled on `doc-extract`'s M6 — which already demonstrates the shape in this portfolio | **6–9 d** total | Nothing. This is the version consistent with why `doc-extract` outranked it |

### Recommendation

**B3, staged: B1 immediately, B2 as one PR, B3's measurement as a second.** B1 first because the
README currently claims eighteen limitations and omits the three that matter, and a false
completeness is worse than a gap — that is this review's recurring finding, applied to itself.

Run under the existing cassette so the attack suite costs **$0**, the same property that makes
variant B in § 4 cheap.

## 6. `token-budget`

908 lines of Python, 11 commits, 4 test files, standard library only, no page. Demoted to Level B
by `0004` § 5, which also rejected building it a page: *rather than build it a page for a stdlib
CLI that proves nothing the other twelve do not, it moves to Level B, where a small proof is what
the tier is for.*

**The recommendation is to spend nothing on it, and to say so rather than invent work.** The tier
decision already resolved the question this session was asked; re-opening it inside a 1–2 month
budget that has a RAG gap and a security debt in it would be the wrong allocation.

One observation recorded for Session 3 rather than acted on here: this is the only project in the
portfolio whose *subject* is the economics of agentic coding, and its README already carries a
measured finding — **~97 % of Claude Code's tokens are cache reads while ~0.5 % output tokens drive
the dollar cost**. That is on-role for an AI Engineer reader and currently reaches nobody, because
the finding lives one click inside a Level B repository. Surfacing it is a **description** problem,
not an extension one, and it costs a line.

## 7. `pl-review-sense`

Given § 3.2, three options:

| | scope | cost | trade-off |
|---|---|---|---|
| **C1 — keep the demotion, rewrite the reason** | The record says "textbook exercise"; make it say what the repository is and why it is still Level B — that the *opening* is weak for the target roles, not the work | **0.5 d**, documentation only | Keeps Session 1's ranking judgment, which was about sixty seconds of a recruiter's attention and is defensible. Removes a reason that the first person to open the repository will contradict |
| **C2 — reverse the demotion** | Back to Level A on the strength of the McNemar test, the challenge set and the cascade costing | **0 d of code**; index and profile copy change | Level A then holds a project whose subject a recruiter for these two roles did not ask for. It also re-opens what `0004` closed, on evidence Session 1 could have read at the time |
| **C3 — repackage the headline** | Keep Level B, but lead with the challenge set rather than with the benchmark: *an 80-sentence Polish adversarial set, and what negation and stripped diacritics do to both models* | **2–3 d** — the work exists; this is a page and a README rewritten around it | The genuinely distinguishing artifact stops being invisible. Overlaps Session 3 and Session 4, so it should be scheduled with them rather than duplicated here |

### Recommendation

**C1 now, C3 scheduled into Session 3.** C1 costs half a day and repairs the record; C3 is where the
value is, and it is a descriptions-and-presentation job that Session 3 owns by definition. C2 is
not recommended: the ranking was about what an opening buys, and nothing in § 3.2 changes that
`apply-scout` and `doc-extract` open better for the roles being targeted.

## 8. Priority

Ordered by value per day inside the 1–2 month budget:

| | item | cost | status | why here |
|---|---|---|---|---|
| 1 | **§ 5 B1** — name `apply-scout`'s three security legs | 0.5 d | **`apply-scout#25`** | An eighteen-item limitations list that omits the three that matter is a false completeness, and it is public today |
| 2 | **§ 7 C1** — rewrite the `pl-review-sense` demotion reason | 0.5 d | **this PR** | Same shape, same cost, and it is a claim in this review's own documents |
| 3 | **§ 5 B2** — confine the loop | 3–4 d | ~~next~~ **on `main`** | The real fix, and the thing B1 is a stopgap for |
| 4 | **§ 4 variant B** — measure the retriever | 4–7 d | ~~after B2~~ **on `main`** | Moves a diagnosis the project has already made in prose into the table where it can regress |
| 5 | **§ 5 B3** — score the attack surface | +3–5 d | ~~after B2~~ **on `main`** | Makes the safety property measured rather than asserted, which is the standard the flagship decision was made on |
| 6 | **§ 7 C3** — repackage `pl-review-sense`'s headline | 2–3 d | Session 3 → **`0006` B6** | Real value, but it belongs to Session 3's pass |

> **Reconciled 2026-09-04 against the repositories, not against this table.** Items 3, 4 and 5 are
> all on `apply-scout`'s default branch: `read_cv.py:55` resolves against a frozen set of permitted
> paths and `fetch.py` holds a scheme allowlist with `check_resolved` on every hand-walked redirect
> hop (B2); `src/apply_scout/retrieval/` prints `eval/expected/retrieval.md` (variant B); and
> `src/apply_scout/attack/` prints `eval/expected/attack.md`, a 5 × 4 × 2 grid (B3). Item 6 is
> carried into [`0006`](0006_session3-4-presentation-block.md) as B6.

**Total for items 1–5: 11–17 days**, revised from 12–18 by § 3.1's correction. That fits the budget
with room, which is the point of leaving variant A and variant C on the table rather than in the
plan — either would consume most of it alone.

## 9. Open items

### Decisions taken 2026-09-03, all as recommended

1. ~~**Which RAG variant** (§ 4).~~ **Variant B** — measure `apply-scout`'s retriever rather than
   build a thirteenth repository. The discoverability objection is answered as part of it (topics,
   repository description, and the page `h1` that family B needs rewritten in Session 4 anyway),
   not left as a residual risk.
2. ~~**Which security level** (§ 5).~~ **B3, staged** — B1 the same day, B2 as one pull request,
   B3's measurement as a second.
3. ~~**`pl-review-sense`** (§ 7).~~ **C1 now, C3 scheduled into Session 3.**

### Executed against those decisions

- **B1 — `apply-scout#25`.** The three legs named in the README's Limitations and in `CLAUDE.md`,
  the latter as a *rule* rather than as prose, because the failure it guards against is a fourth
  unbounded tool argument being added by someone reading the existing two as precedent. Found in
  the same pass: the README claimed **188 tests** in two places against a measured **195**, and
  `0004` § 4 said **194** — one number, three surfaces, none of them right.
- **C1 — this pull request.** `0004` § 5's reason rewritten rather than merely marked contested.

### Still open

- ~~**B2 — confine the loop.** The next change, and the thing B1 is explicitly a stopgap for. Not
  started; `apply-scout#25` says so in the README rather than implying a fix that has not landed.~~
  **Landed, and so did B3.** Both are on `main` as of 2026-09-04 — see the box in § 8 for the
  evidence in source. ADR-0012 (*the page quotes the artifacts*) was written **after** them, which
  is the clearest single proof that this bullet had gone stale: the project produced a decision
  record about publishing what B3 measured while this line still said B2 had not started.
- ~~**Carried from `0003` § 9: every `LICENSE` names the handle `P0w3r223` while the profile now
  carries a legal name.**~~ **Closed 2026-09-04.** Applied to all twelve together, as decided —
  `Copyright (c) 2026 Piotr Cząstkiewicz` — and verified from the API on the default branches *after*
  the merges, not from the pull requests. [`0006`](0006_session3-4-presentation-block.md) § 6 decision 2
  carries the twelve SHAs. This bullet stayed open through one earlier draft that struck it on the
  strength of the decision alone; it is struck now on the strength of twelve merges.

  *An earlier draft of this line struck the bullet on the strength of the decision. That is the
  failure this document exists to name — a state asserted because it was agreed rather than because
  a repository shows it — and it is left visible rather than tidied away. `0003` § 9 decision 5 was
  correct all along and now agrees with this line again.*
- ~~**Carried:** `ab-lab`'s `refresh.yml` was bumped to the current action majors but runs weekly on a
  schedule and has not fired since — next firing ~2026-09-07, so no check has exercised it.~~
  **Dispatched by hand 2026-09-04** rather than waited on: the workflow already declares
  `workflow_dispatch`, so nothing had to change to exercise it, and waiting would have carried an
  unexercised bump into a third session. `0006` § 6 decision 3.
- ~~**`car-price-ml#21`** is green and awaiting merge. The language bar only re-computes once the
  change is on the default branch, so that verification belongs on `main`, not on the PR.~~
  **Merged as `6e6019f`, and the check was run where it had to be.** `Jupyter Notebook` is gone
  from the languages API entirely, `.language` reads `Python`, and the other five figures are
  byte-identical to the pre-merge reading (207 665 / 11 071 / 8 624 / 1 844 / 798) — so the notebook
  left the language bar and nothing else moved. `#48` re-points the submodule.
- ~~**Found while reading `apply-scout`, not yet owned:** its README and `CLAUDE.md` both still open
  *"Portfolio project **P3** (the flagship)"*, which `0004` § 5 withdrew when `doc-extract` took the
  role and `apply-scout` lost the ⭐. The decision is merged into the index and the repository that
  is subject to it still asserts the old status. Left for a decision rather than fixed in `#25`,
  because rewriting how a project introduces itself is a presentation call and Session 3 owns those
  — but it is a false statement in the meantime, not a stylistic one.~~ **Closed on the two surfaces the finding named, and still open on a
  third it did not.** `apply-scout#32` removed it from the README and from `CLAUDE.md`. But
  `src/apply_scout/__init__.py:5` still opens *"Portfolio project P3 (the flagship). The public
  surface is intentionally small in this first milestone…"*, and the same docstring still says
  *"Real tools and the evaluation harness arrive in later milestones"* — of a repository that has
  shipped both. **So the finding stands, on the package's own docstring**, and it carries into
  [`0006`](0006_session3-4-presentation-block.md) B6 with the other text layers.

  *A draft of this line said the only surviving occurrence of "flagship" was an unrelated comment
  about a trajectory artifact. That was a grep over `README.md` and `CLAUDE.md` reported as a grep
  over the repository; `git grep -i flagship` returns the docstring above. Recorded rather than
  quietly widened, because "I checked" and "I checked everywhere" are the two statements this
  review keeps finding substituted for one another.*

  The reason in the record was corrected at the same time: the `P3` **slot** is not false — `0004` § 5 kept it — its
  legend simply lives in a private repository, so a public README asserting it explains nothing to
  the only reader who can see it.

### Reconciliation, 2026-09-04

Every bullet above was re-read against the repositories before Session 3 opened, per `0003` § 9.
**Four of the five were stale, all because work landed and this document did not follow** — the
direction § 8 and § 9 of the plan both named. `0003` § 11 records the pass in full, including the
mirror-image failure this one also found: work that quietly got *done* outside the session that
owned it, which over-states the next block rather than under-stating it.

Sessions 3 and 4 are designed together as one block in
[`0006_session3-4-presentation-block.md`](0006_session3-4-presentation-block.md). **That is where
the next session starts.**
