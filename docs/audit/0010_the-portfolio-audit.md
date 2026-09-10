# The portfolio audit

Date: 2026-09-10
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: [0003](0003_portfolio-review-plan.md) (the earlier multi-session plan),
[0009](0009_the-review-of-the-whole-system.md) §7, [ADR-0004](../adr/0004_what-carries-the-page-spec.md)

---

## 1. What this is, and what it is not

The state of a multi-session audit: thirteen repositories, the profile README, and four
private repositories swept for secrets only.

This document is the **state**. `0010_scan-prompt.md` is the **method**;
`0010_repair-prompt.md` is the **authority to act**. A figure written here is frozen the
moment it is written, with the command that produced it beside it — `ADR-0004` §5's rule,
which is why `0007` §3 was corrected five times before the split.

It is **not** a findings report. A finding lives in §4's row until a repair session closes
it; §5 holds only what recurred across repositories.

**Why the audit is split this way, and what it cost to find out.** A first version of the
scan prompt was written on 2026-09-10, reviewed against `agent-engineering-guide`, and then
counter-reviewed by two fresh-context agents asked to refute it. Of twelve self-made
findings three were refuted outright, five overstated, and of the three that survived, all
three carried a wrong or incomplete repair. The counter-reviews raised about fourteen
defects the self-review had missed — four of them critical, including that this document
did not exist while the prompt's first sentence sent every session to read it. §3.1's
scan/repair split is what both reviews converged on independently.

## 2. The state this was opened against

Index `2cb5d45` on `main`, level with origin, twelve pointers matching their own
`origin/main`, nothing uncommitted, no open portfolio pull request. S14a closed the same day
(`1ba8975`, `a0d19cb` #32, `d440ab0` #10, `2cb5d45` #115); S14b remains open.

### 2.1 The corpus

`git ls-files`, `git rev-list --all --count`, `git ls-remote origin 'refs/pull/*/head'`.
`unreach` counts PR-head commits that `rev-list --all` does not contain.

| repo | files | py LOC | md | commits | PR refs | unreach |
|------|------:|-------:|---:|--------:|--------:|--------:|
| `current_projects` (private) | 73 | 12 255 | 20 | 157 | 115 | 115 |
| `ab-lab` | 64 | 8 617 | 14 | 67 | 17 | 9 |
| `apply-scout` | 114 | 11 713 | 20 | 116 | 32 | 23 |
| `auth-log-scan` | 32 | 1 882 | 2 | 28 | 13 | 10 |
| `car-price-ml` | 71 | 4 739 | 11 | 148 | 31 | 14 |
| `doc-extract` | 274 | 26 100 | 86 | 57 | 15 | 14 |
| `it-job-radar` | 86 | 7 432 | 9 | 119 | 36 | 35 |
| `mini-traceroute` | 39 | 0 | 3 | 25 | 10 | 7 |
| `mlops-car-price` | 57 | 4 859 | 13 | 34 | 18 | 17 |
| `pl-jobs-lora` | 82 | 7 266 | 11 | 63 | 18 | 17 |
| `pl-review-sense` | 69 | 5 690 | 7 | 48 | 19 | 19 |
| `token-budget` | 21 | 908 | 2 | 15 | 5 | 4 |
| `wroclaw-air-insights` | 72 | 11 760 | 6 | 151 | 40 | 40 |
| **total** | **1 054** | **103 221** | **204** | **1 028** | **369** | **324** |

**209 of those unreachable commits are in the twelve public repositories**, and GitHub keeps
`refs/pull/*/head` indefinitely — so a sweep bounded by `rev-list --all` misses commits
anyone can still fetch. This portfolio squash-merges, which is what puts every branch commit
there. §3.4's E1 fetches them first for that reason.

### 2.2 The surfaces

`python -m tools.pagespec --detail`, the run `--only` cannot take because it suppresses both
censuses.

Eleven committed surfaces all read `clear` (4 or 5 `undecided` each); `wroclaw-air-insights`
reads `clear, 5 undecided` on the wire under `--fetch`. Gate exits 0.

- **separator census** — portfolio 95 figures, 95 separators, one each.
- **role census**, `border` family — `--border` 60 (78 %), `--warn` 8 (10 %), `--accent` 3,
  `--danger` 3, `--border-control` 2 (3 %, `car-price-ml/app` and `mini-traceroute`),
  `--positive` 1. The `--border-control` row is S14a, landed the same day.

### 2.3 Axis E1 across the whole portfolio — the shallow pass

Run once here rather than thirteen times, because a credential pattern is a portfolio
question. Tree and full history including PR heads, thirteen repositories.

**Clean.** Three matches, all read and all explained:

| where | what | verdict |
|---|---|---|
| `apply-scout/src/apply_scout/attack/payloads.py:40` | `SECRET_MARKER = "BEGIN OPENSSH PRIVATE KEY"` | a canary string for the exfiltration suite |
| `apply-scout/src/apply_scout/attack/suite.py:133` | writes that header, with no key material | bait for the same suite |
| `apply-scout/eval/cassettes/eval.jsonl` | `GOOGLE_PICKER_DEVELOPER_KEY` | GitHub's own public client key, in a recorded response |

The cassette records `api.github.com`, `github.com`, `job-boards.greenhouse.io`,
`jobs.smartrecruiters.com`, `cdn.lever.co` and `jobs.lever.co`. The Picker key is
client-side and public by design; it is not the owner's, and it is an E2 question about
recorded third-party content rather than an E1 one.

### 2.4 Axis E0 — commit metadata

`git log --all --format='%an <%ae>%n%cn <%ce>' | sort -u`. Three identities everywhere
(`P0w3r223`, `Piotr Cząstkiewicz`, `GitHub`), plus `github-actions[bot]` in
`wroclaw-air-insights`. See §4's first row.

## 3. The method

### 3.1 Sessions

| # | Session | Kind |
|---|---------|------|
| 0 | this document | done |
| 1–12 | one submodule each | scan |
| 13 | `current_projects` — `tools/`, `tests/`, `docs/` | scan |
| 13b | `P0w3r223/P0w3r223` — the profile README | scan |
| 13c | `infra-docker`, `infra-docker-powiadomienia-teams`, `infra-docker-workmate`, `student-wellbeing-pwr` | secrets only |
| R1…Rn | repair sessions, driven by §4 | repair |

Order for 1–12: `auth-log-scan` (pilot — small, all five axes), `apply-scout`,
`it-job-radar`, `pl-jobs-lora`, `doc-extract`, `ab-lab`, `mlops-car-price`, `car-price-ml`,
`pl-review-sense`, `wroclaw-air-insights`, `mini-traceroute`, `token-budget`.

A scan session never repairs; a repair session never reads a repository's raw data
artifacts. The split is why a scan session may read a GitHub issue body, a scraped dataset
or an extraction corpus without that content reaching anything that can act.

### 3.2 Identifiers for axis E2 — sources, never values

Writing a PESEL or a postal address here would create the exposure the audit exists to find.

| identifier | source |
|---|---|
| git author name and e-mail | `git config user.name`, `git config user.email`, §2.4 |
| private e-mail, phone, address, employer names | `audit-identifiers.local` — untracked, gitignored, written by the owner before session 1 |
| national-ID / bank-shaped numbers | shape only, matched by pattern |

A session that finds `audit-identifiers.local` absent records E2 as `blocked` and does not
guess. Guessing is how E2 degrades to whatever the session happens to know.

### 3.3 Per-repository commands

Four of the fifteen sessions cannot run the obvious one. Verified 2026-09-10.

| repo | surface key(s) | page command | tests |
|---|---|---|---|
| `token-budget` | none | — `--only token-budget` exits 2, `no surface named` | `pytest` |
| `current_projects` | none | full `pagespec --detail`, which is the census run | `pytest` |
| `car-price-ml` | `car-price-ml`, `car-price-ml/app` | **two runs**, one per key | `pytest` |
| `wroclaw-air-insights` | `wroclaw-air-insights` | **`--fetch` required** — without it the run exits 0 having read nothing | `pytest` |
| `mini-traceroute` | `mini-traceroute` | `--only mini-traceroute` | **CTest, not pytest** — no Python at all; `pytest` collects nothing and exits 5 |
| the rest | the repo name | `--only <repo>` | `pytest` |

`car-price-ml` additionally generates `docs/app/styles.css` and `docs/index.html` from
`src/car_price_ml/site/assets/`; edit the source and run `python -m car_price_ml.site.build`,
or `test_the_committed_form_assets_match_the_source` fails.

### 3.4 Verdicts

`clear` · `finding` · `blocked` · `not checked`, for all five axes.

`blocked` is an instrument that would not answer — tests that will not collect, `gh` rate
limited, a page answering 4xx, `audit-identifiers.local` missing. A blocked axis is not a
clean axis: the repository returns to the queue.

Axis E carries a severity: `metadata` · `third-party data` · `credential` · `personal data`.

### 3.5 The threshold

**Repair in one pass** — all of: confined to one repository plus a pointer bump; no new
module, signature or public API; where the repo has a surface, its §3.3 command is no worse
before → after; covered by an existing test, or a guard added in the same pull request and
proven red by §3.6.

**Its own row and its own pass** — any of: more than one repository; a new clause, a new
guard in `tools/`, or a change to `0007`; a published figure an artifact must be re-run to
produce; a design decision (→ `architect`); a credential rotation, a history rewrite, or a
deletion of published data.

When unsure, leave the row open. A row costs a line; a half-finished repair costs a stage.

### 3.6 The mutation battery — three observations

`0008` §4 records two traps a one-observation battery walks into.

1. The guard **collected and green** on unmutated code — `1 passed`, not `no tests ran`.
   A broken `-k` gives exit 5, which reads as red (`0008`:2351).
2. The mutation red **on that guard's own assertion**, not on any non-zero exit.
   `tests/conftest.py:119` skips when a submodule is absent, and *a skip is a pass*
   (`0008`:2347).
3. Green again after reverting. Commit before mutating — the `git checkout --` that reverts
   discards uncommitted work.
4. Run the mutated code with `-B`, or delete `__pycache__` first. CPython validates a `.pyc`
   on mtime-in-seconds **and size**, so a mutation that preserves file length — `any`→`all`,
   `<`→`>`, `and`→`or`, the cleanest ones — can execute stale bytecode and report green over a
   mutation that is really red. Found 2026-09-10 by the review closing S14b, on its own
   battery, on exactly such a mutation.

And do not pass `-q`: in this environment it suppresses the `N passed` summary line, so a
parser reading it scores a passing run as an empty one. S14b's first battery reported all nine
mutations `BASELINE BAD` for that reason and no other — which is observation 1 working.

## 4. The rows

Written **after each axis**, not at the end. `Index SHA` is `git rev-parse HEAD` of this
repository at the time of the scan — not "the main SHA": the checker that produced the axis
C verdict is the one at that HEAD.

| # | Repo | Index SHA | E | A | B | C | D | Open | Not checked |
|---|------|-----------|---|---|---|---|---|------|-------------|
| — | *portfolio-wide* | `2cb5d45` | `finding` · metadata | — | — | — | — | R-1 | — |

### R-1 — the real name in commit metadata, twelve public repositories

**113 commits** across the twelve carry `Piotr Cząstkiewicz` in the author or committer
field. Measured 2026-09-10 with
`git log --all --format='%H %an %cn' | grep -c 'Cząstkiewicz'`, counting commits and not
fields — an earlier count of the same thing read 111 by counting fields and by predating the
day's two sibling merges, which is why the command is written down beside the figure.

| repo | of | | repo | of |
|---|---|---|---|---|
| `apply-scout` | 13 / 116 | | `mlops-car-price` | 9 / 34 |
| `wroclaw-air-insights` | 13 / 151 | | `pl-jobs-lora` | 9 / 63 |
| `car-price-ml` | 12 / 148 | | `doc-extract` | 8 / 57 |
| `auth-log-scan` | 10 / 28 | | `pl-review-sense` | 8 / 48 |
| `ab-lab` | 9 / 67 | | `token-budget` | 4 / 15 |
| `it-job-radar` | 9 / 119 | | | |
| `mini-traceroute` | 9 / 25 | | | |

`current_projects` carries 70 of 157, and is private.

**Why the sweep the audit was first given would have missed this.** `git grep` reads blobs;
commit metadata is not a blob. The first version of the scan prompt swept only blob content
and would have reported every one of the twelve clean on the axis it itself called *"the
likelier one in a portfolio built from a CV"*.

**Open, and it is the owner's decision, not the audit's.** The repair is a history rewrite of
twelve public repositories: every SHA changes, every existing link to a commit breaks, and
every figure this record cites by SHA has to be re-derived. It is also arguable that a name
on a public CV portfolio is not an exposure in the sense a token is. §3.5 puts a history
rewrite in the second column regardless, so nothing happens here without an explicit
instruction. What this row buys is that it is a decision rather than an oversight.

## 5. Cross-cutting

What recurred rather than happened once. A per-repository split cannot see a pattern by
construction; this section and §2's baselines are where patterns accumulate.

- **§2.3, E1 across all thirteen: clean.** Sweeping once rather than thirteen times is what
  made the three matches cheap to read together and dismiss together.
- **Two repositories carry a deliberate attack corpus** — `apply-scout/src/apply_scout/attack/`
  and `doc-extract/results/attack-*/`. Both are self-authored, non-adaptive, and versioned;
  neither is content an outsider controls. Sessions 2 and 5 will read them, which is why
  those sessions are scans and cannot act.

## 6. Corrections, and which prompt version they bind

The scan and repair prompts carry a version stamp. A correction here **outranks the prompt**
from the version named onward — otherwise the operator keeps pasting a prompt this document
has already contradicted.

| date | binds | what was wrong | what replaces it |
|------|-------|----------------|------------------|
| 2026-09-10 | v1.0 (never used) | `git grep` over blobs cannot see commit metadata; the E2 half of the sweep returned zero on the one exposure that certainly exists | §3.4's E0, and R-1 |
| 2026-09-10 | v1.0 (never used) | `rev-list --all` misses 209 publicly fetchable PR-head commits | E1 fetches `refs/pull/*/head` first |
| 2026-09-10 | v1.0 (never used) | `--only wroclaw-air-insights` exits 0 having read nothing, which is indistinguishable from a pass | §3.3 requires `--fetch` there |
