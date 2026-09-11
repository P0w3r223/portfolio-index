# The portfolio audit

Date: 2026-09-10
Status: accepted
Author: Piotr Cząstkiewicz
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

**This baseline was taken about an hour before S14b, and a session reading it will not see
what it says.** §2 is frozen by `ADR-0004` §5 and stays as measured — but S14b (`e3a7f31`,
`#117`) gave `contrast marks` a verdict, and at that commit **five of the eleven read
`1 fail`**: `ab-lab`, `auth-log-scan`, `car-price-ml`, `it-job-radar`, `pl-review-sense`. The
run still exits 0 because the key is `report-only`, and the reason is printed under
`gate policy` on every run. **The `undecided` counts moved with the verdict and the whole
sentence above is stale, not half of it**: `ab-lab` reads 2, the other ten read 3, and
`wroclaw` under `--fetch` reads 4 — not the 4-or-5 and 5 the line records. So a scan
session's axis C compares its own `--only` output against the checker in front of it, never
against this line; the number a row quotes comes from the run it made. Verified 2026-09-10 at
`e3a7f31`: 619 tests green, gate 0, 153 marks below 3.0:1 of 739 measured, and `--fetch`
reports no `served` mismatch on any of the twelve.

**The two censuses below are not stale, and the reason is worth stating because checking it
misleads.** Both reproduce byte-for-byte at `e3a7f31` — S14b moved neither. But this
paragraph has just quoted a `--fetch` figure for `wroclaw` inside a block whose header names
the *fetchless* run, and a reader who reaches for `--fetch` to check it sees `portfolio 98`
and `--border 69` against the bullets' 95 and 60. That is the twelfth surface joining the
census, not three more moved figures: `--fetch` judges all twelve, and §2.2's own header
names `--detail` without it for exactly that reason. Found by the review of this erratum,
which walked into it.

*The gap is 54–70 minutes — `2cb5d45` merged 13:05, `69531b4` wrote this section 13:21,
`e3a7f31` merged 14:15. The first version of this erratum said "hours", twice, in a
correction whose entire argument is that figures come from instruments and not from a hand.*

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
| 13 | `current_projects` — `tools/`, `tests/`, `docs/`, **and the tracked files at the root** | scan |
| 13b | `P0w3r223/P0w3r223` — the profile README | scan |
| 13c | `infra-docker`, `infra-docker-powiadomienia-teams`, `infra-docker-workmate`, `student-wellbeing-pwr` | secrets only |
| R1…Rn | repair sessions, driven by §4 | repair |

*Session 13's row gained its root clause 2026-09-10: `pyproject.toml`, `.gitignore` and the
workflow are tracked, are this repository's, and fell outside all three named directories. The
audit repairs that class of disagreement elsewhere, and had just created one of its own. The
clause named a fourth file, the identifier template, which was deleted 2026-09-11 with §3.2.*

Order for 1–12: `auth-log-scan` (pilot — small, all five axes), `apply-scout`,
`it-job-radar`, `pl-jobs-lora`, `doc-extract`, `ab-lab`, `mlops-car-price`, `car-price-ml`,
`pl-review-sense`, `wroclaw-air-insights`, `mini-traceroute`, `token-budget`.

A scan session never repairs; a repair session never reads a repository's raw data
artifacts. The split is why a scan session may read a GitHub issue body, a scraped dataset
or an extraction corpus without that content reaching anything that can act.

### 3.2 Identifiers — retired 2026-09-11

**The identifier sweep is gone, on the owner's decision, and this heading is kept only so
§3.3 to §3.6 keep their numbers** — every one of them is cited by number from the prompts and
from `CLAUDE.md`.

What stood here was a table of sources for the owner's private identifiers, a working copy
named `audit-identifiers.local`, a committed template, and six guards in
`tests/test_audit_identifiers.py` keeping the two honest. All of it is deleted. Axis E keeps
E0 and E1; **E2 survives as third-party data only** — whose data a committed artifact holds,
under what licence, whether it names identifiable people, and whether it is served publicly —
and that half needs nothing from the owner.

**The reason, recorded because a later session will otherwise rebuild it.** The sweep used the
owner's private values as search literals across thirteen trees and their history. The design
protected them by never committing the file and by recording only a count in a §4 row — but it
could not protect them from the one thing the sweep requires, which is that a session **read**
them, putting a phone number or a postal address into a conversation transcript. Offered the
alternatives — supply nothing, supply only low-sensitivity values, or run the sweep himself and
report counts — the owner chose to supply nothing and to retire the axis. **A permanently
blocked axis was also the worse engineering outcome**: §3.4 sends a repository with a blocked
axis back to the queue, so carrying E2 unfillable made the whole twelve-session queue
unstartable.

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
limited, a page answering 4xx. A blocked axis is not a clean axis: the repository returns to
the queue.

*This definition carried a fourth instrument until 2026-09-11 — the identifier file, absent or
supplying no value — and it is gone with §3.2. It was also the only one of the four that could
never be unblocked by anything a session does, which is why retiring the axis was the better
outcome than carrying it: every repository in the queue would have returned to the queue.*

*The retired clause read only `missing` until 2026-09-10, which is the wording §3.2's own
correction called too narrow — and this is the section both prompts send a session to by name
for what `blocked` means, so a session consulting it would have got the pre-correction
answer while §3.2 held the wider rule. Two sections of one document disagreeing is not
something §6 can route around: §6 corrects the prompts, not this file.*

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

### 3.6 The mutation battery — six observations

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
5. **Revert by bytes, not by text.** `Path.read_text()` folds CRLF to `\n` and
   `Path.write_text()` re-expands it, so a battery that round-trips a file through text leaves
   it byte-different from what it restored — `core.autocrlf` is `true` here and there is no
   `.gitattributes`, so `git status` then reports a file the battery believes it put back.
   `read_bytes`/`write_bytes`. Found 2026-09-10 by this battery, on itself.
6. **A guard can be vacuous because the tool it shells to excludes its subject by default**,
   and only a mutation says so. `tests/test_audit_identifiers.py` asserted that `.gitignore`
   does *not* reach the committed template — with `git check-ignore`, which skips paths already
   in the index, because tracked files are not subject to exclude rules. The template is
   tracked, so the assertion answered *not ignored* whatever the pattern said and **could not
   fail**. It went green over the mutation written to redden it. `--no-index` asks the question
   the assertion meant. Found 2026-09-10 by the battery for that file, which is the only reason
   it was found: the guard read correctly, ran, passed, and proved nothing.

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
| 1 | `auth-log-scan` | `dc04541` | `finding` · metadata (R-1) | `clear` | `finding` | `clear` | `clear` | A-1 | §5's cross-repo half |

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

### A-1 — `auth-log-scan`, session 1, the pilot

Scanned 2026-09-11 at index `dc04541`, gitlink `50e8b6e`, entry state clean. Four axes, because
§3.2's identifier half was retired the same day; E here is E0 and E2's third-party question.

**E — `finding` · metadata, and it is R-1's, not this repository's own.** Ten of twenty-eight
commits carry `Piotr Cząstkiewicz` in the author or committer field, which reproduces R-1's
table cell exactly. Nothing else: **every address in both bundled logs and on the published
page is in a documentation range** — RFC 5737 for IPv4, and `2001:db8:2::19` for IPv6 — with
the one exception of `0.0.0.0`, which appears as `Server listening on 0.0.0.0 port 22` and is a
bind address rather than a host. Account names are invented service names. `README.md`:133
claims exactly this, and the claim was checked against the artifacts rather than taken: it
holds in both halves. *The IPv6 half nearly became a false finding — a first sweep used a
pattern that cannot match compressed notation and reported zero `2001:db8::/32` addresses,
which would have recorded the README as overstating. `FG-1`, caught by asking why a claim so
specific would be wrong.*

**A — `clear`.** 42 tests pass. No bare `except` and nothing swallowed, no `Any`, `print` only
in the CLI entry point, thresholds in `config.py` rather than inline. Five functions exceed
`good-practices.md`'s fifty lines — `render` 107, `analyze` 71, `window_chart` 59, `main` 55,
`render_terminal` 53 — and only `render` reads as more than one job, because it orchestrates
read → parse → analyze → chart → payload in one body. `analyze` mutates a local accumulator,
which is a fold and not shared state.

*One observation, deliberately not a finding.* `tests/test_site.py:263`
(`test_the_bands_are_still_visible_against_the_lane_they_sit_on`) puts **every** assertion
inside a loop over `_painted(css, _BAND_SELECTOR)`, so an empty match passes it silently. It is
not vacuous today, because the sibling test at `:237` pins `len(bands) == 2` and would redden
first — but the protection lives in a different test, so a mutation battery would report the
property caught while the guard that names it proved nothing. `SG-1`'s shape at one remove.

**B — `finding`.** Two, and the first has a date on it.

**The README's quoted sample output reproduces today only because today is 2026.** The bundled
log is traditional syslog and carries no year, `cli.py`:74 defaults `--year` to
`datetime.now().year`, and the block README quotes prints `2026-03-10` in seven places. Run on
1 January 2027 it prints `2027-03-10` and the README is wrong in all seven, with nobody having
touched the repository. **The page does not have this problem**: `site/build.py`:36 pins
`DEMO_YEAR = 2026`, so the repository already holds the fix one file over and did not apply it
to the README. Verified by running the same command with `--year 2027`.

*Measured before leaving it in §4 rather than promoting it: the shape does not recur.* Five
repositories call `datetime.now()` in Python — `ab-lab`, `apply-scout`, `auth-log-scan`,
`car-price-ml`, `it-job-radar` — and of their twenty-five fenced README blocks exactly two
carry a 2026 date. One is this finding; the other is `it-job-radar`'s `--seed 20260814`, a
literal a reader types rather than a value the code derives, which is a different shape. So
**one occurrence, and §5 gets nothing** — §5 holds what recurred, and a single incident
belongs in this row. Run once here rather than eleven times, on `0010` §2.3's precedent.

**`--min-success-failures` is documented nowhere.** The CLI accepts it; `README.md` returns
zero occurrences. Every other flag the README names exists, every command it gives runs, and
its quoted output otherwise matches byte for byte.

**C — `clear`, with one measured `FAIL` that belongs to a decision and not to this page.**
`python -m tools.pagespec --only auth-log-scan` reads `1 fail, 3 undecided`; the fail is
`contrast marks`, 13 of 311 measured below 3.0:1, a `report-only` key whose remaining
population `0008` §4.29 and `ADR-0008` §10 have already partitioned into open design questions.
Nothing here is new and nothing here is this session's to repair.

The text is strong on a recruiter's reading. The `h1` — *"108 failed logins in 7.1 hours — and
only some of them are an attack"* — carries a figure, its unit and the claim, and the first
screen says what the page is and what it proves. **Its quoted terminal block reproduces to the
character**, which is `0007` §5.0 satisfied where nothing carries it: 146 events, the range
`00:12:03 .. 07:16:40`, `108 / 5 / 33`, four brute-force sources, and 7h04m is the 7.1 hours
the headline names. No figure on the page lacks a unit or a baseline, and no sentence needed a
second reading.

**D — `clear`.** MIT licence tracked, homepage set to the Pages URL, six relevant topics, a
description carrying the same claim as the `h1`, no open issues, `main` the only branch, CI
green on its last three runs. This repository was among the nine clean of `0010` §2.4's
sweep and still is.

**The cheapest observation that would falsify each `clear`.** For A: run the mutation battery
over `tests/test_site.py` and see whether `:263` reddens on its own assertion rather than
`:237`'s. For C: a `--fetch` run, which judges the served bytes rather than the committed file
— this scan read the committed one. For D: `gh api` for branch protection and for the Pages
build source, neither of which `gh repo view` reports.

**Not checked.** The cross-repository half of §5 — whether this repository's shapes recur
elsewhere — which is not a session-1 question by construction. The `contrast marks` population
was read from the checker's summary rather than site by site. And no artifact under
`docs/` other than `index.html` was read, because there is none.

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

**One row is a state erratum rather than a prompt correction, and its `binds` cell says so.**
Nothing in either prompt contradicts §2.2's baseline: the scan prompt already tells axis C to
run §3.3's command *before* judging any text. It is registered here because §6 is the only
part of this document a session is routed to unconditionally — the prompts send a reader to
§3, §3.3, §3.4 and its own row in §4, and never to §2.2, so a warning left there is a warning
that does not arrive. Taken deliberately on the review of 2026-09-10, which raised it as a
question rather than as a defect.

| date | binds | what was wrong | what replaces it |
|------|-------|----------------|------------------|
| 2026-09-10 | v1.0 (never used) | `git grep` over blobs cannot see commit metadata; the E2 half of the sweep returned zero on the one exposure that certainly exists | §3.4's E0, and R-1 |
| 2026-09-10 | v1.0 (never used) | `rev-list --all` misses 209 publicly fetchable PR-head commits | E1 fetches `refs/pull/*/head` first |
| 2026-09-10 | v1.0 (never used) | `--only wroclaw-air-insights` exits 0 having read nothing, which is indistinguishable from a pass | §3.3 requires `--fetch` there |
| 2026-09-11 | **v3.0** | the prompt's E2 sweeps the owner's personal identifiers, which the owner has declined to supply — so the axis could never be anything but `blocked`, and §3.4 would have returned every repository in the queue | **The identifier half is retired**, with its template, its six guards and §3.2's sources table deleted. E2 is third-party data only; E0 and E1 are unchanged. §3.2 holds the reason. *This row replaces the v2.0 one it supersedes, which corrected the placeholder rule for a file that no longer exists* |
| 2026-09-10 | **v2.0**, as a warning and not a contradiction | §2.2's surface baseline was measured at `2cb5d45`, about an hour before S14b gave `contrast marks` a verdict; a session quoting it would write `clear` into a row where its own run prints `1 fail`, with the `undecided` counts moved too | §2.2's erratum — axis C quotes the run the session made, and the key is `report-only`, which is why the gate still exits 0. **No count is given here on purpose**: this cell said *five of the eleven* until 2026-09-11 and was stale within hours of being written, because `ADR-0008` §10 took the marks census 88 → 26 the same evening and `it-job-radar` went clean. A warning about what a session's own run prints must not carry a figure the session's own run contradicts |
