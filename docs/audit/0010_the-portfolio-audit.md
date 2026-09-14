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

**The `Open` column lists the rows a repository raised, closed ones included, and the axis
cells stay as measured.** Both are the frozen-at-HEAD rule above, and neither is a live status:
a `B` cell reading `finding` beside an `Open` cell reading `A-1 closed` is a scan's verdict
beside a repair's, not a contradiction. The row body says which. *Written on review, 2026-09-11,
when the first closure landed and the header read literally as a list of what is still open.*

| # | Repo | Index SHA | E | A | B | C | D | Open | Not checked |
|---|------|-----------|---|---|---|---|---|------|-------------|
| — | *portfolio-wide* | `2cb5d45` | `finding` · metadata | — | — | — | — | R-1 | — |
| 1 | `auth-log-scan` | `dc04541` | `finding` · metadata (R-1) | `clear` | `finding` | `clear` | `clear` | **A-1 closed** · R-1 stands | §5's cross-repo half |
| 2 | `apply-scout` | `5278b1b` | `finding` · metadata (R-1) · third-party data | `clear` | `finding` | `clear` | `finding` | **E-2 and B-2 closed** · D-2 part-closed · R-1 stands | four ADRs, the `llm` cassette half, the judgment set |
| 3 | `it-job-radar` | `5664e43` | `finding` · metadata (R-1) · third-party data | `clear` | `finding` | `finding` | `finding` | **E-3 and B-3 closed** · D-3's tree sites closed, its GitHub half open · C-3 open · R-1 stands | the notebook, `docs/plan/` and `docs/ideas/`, the Parquet row values |

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

**Closed 2026-09-11 by `auth-log-scan` `1d02f6f` (#14), index pointer bumped in the commit
carrying this line.** Both B findings repaired in one pass under §3.5: one repository plus a
pointer bump, no new module or signature, and the §3.3 page command reads identically before
and after — the page was never in scope. **Three guards where nothing read the README at all**,
plus a positive control the review asked for; six mutations, each red on its own assertion over
a collected-green baseline, green after reverting. *The unit matters and changes below*: that is
four test functions, which `pytest` collects as six because one is parametrised over three
years. **42 collected → 48.**

**The repair falsified a figure while repairing one, and the `code-reviewer` pass is the only
reason that is a sentence here rather than a finding for session 13.** `README.md`:122 **at the
scanned gitlink `50e8b6e`** claimed *"42 in the suite as a whole"*, which the first commit's five
collected cases made 47 — a change whose stated
purpose was that the README stops being wrong on its own, shipping a README wrong on arrival,
one paragraph below the defect it was closing. Removed rather than corrected, on `#125`'s
precedent: a hand-typed figure with no instrument beside it is the defect, and correcting it
only sets the next staleness date. `docs/reference/failure-classes.md` FG and ST-3.

**The A-axis observation was not taken and stays open as an observation.** `tests/test_site.py`:263
still puts every assertion inside a loop that an empty match satisfies — `SG-1` at one remove.
It is not vacuous today and repairing it is not a B finding; it belongs to whichever pass runs
the mutation battery this row names as the cheapest falsifier of `A: clear`.

Scanned 2026-09-11 at index `dc04541`, gitlink `50e8b6e`, entry state clean. Four axes, because
§3.2's identifier half was retired the same day, so E is E0 and E2's third-party question.
*This opened* **“Four axes”** *until 2026-09-11.* §3.1 and §3.4 both say five, this row carries
five lettered subsections, and §4's table has five columns: §3.2 retired half of E2, not an axis.

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
not vacuous today, because the sibling test pins `len(bands) == 2` at `:240` and would redden
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
`:240`'s. For C: a `--fetch` run, which judges the served bytes rather than the committed file
— this scan read the committed one. For D: `gh api` for branch protection and for the Pages
build source, neither of which `gh repo view` reports.

**Not checked.** The cross-repository half of §5 — whether this repository's shapes recur
elsewhere — which is not a session-1 question by construction. The `contrast marks` population
was read from the checker's summary rather than site by site. And no artifact under
`docs/` other than `index.html` was read, because there is none.

### A-2 — `apply-scout`, session 2

Scanned 2026-09-11 at index `5278b1b`, gitlink `c7958eb`, entry state clean and `HEAD`
identical to `origin/main`. **Five axes**, E being E0 and E2's third-party half — §3.2 retired
half of E2, not an axis, and this line said *four* until 2026-09-11.

**E0 — `finding` · metadata, and it is R-1's.** Three identities in the history and no
fourth: `P0w3r223 <p0w3r2243@gmail.com>`, `Piotr Cząstkiewicz <p0w3r2243@gmail.com>` and
GitHub's noreply. **13 of 116** commits carry the real name, which reproduces R-1's table cell
exactly. The address is the portfolio's published contact and is not a finding.

**E2 — `finding` · third-party data. The repository redistributes five companies' pages
verbatim under a blanket MIT notice.** `eval/cassettes/` commits **1 818 808 characters of
raw job-board HTML** across **nine** `http` records over eight distinct URLs — six live
pages, one of them recorded twice, and two `{"error": "HTTP
404"}` — from **Allegro** (two postings, SmartRecruiters), **tryjeeves** (Lever), **Zapier**
(Ashby), **KONUX** and **Reddit** (Greenhouse). **The Athletic** and **HHAeXchange** are named
by the two 404 records and contribute no page content at all, so a provenance note must not
attribute anything to them. `LICENSE`
reads *MIT / Copyright (c) 2026 Piotr Cząstkiewicz* over the whole tree, and **nothing
reconciles the two**: no file carves the recorded pages out of the grant. *This sentence also
said* **“and no company is named anywhere in the repository”** *until 2026-09-11, and that was
the fourth universal quantifier in this row and the most easily refuted:* `README.md`:167
names both 404 companies in prose, five `docs/decisions/*.md` and both `eval/` data files carry
`reddit-`, `konux-`, `allegro-` and `zapier-` task ids, and **this row's own positive control
counts `reddit` 108 times and `Allegro` 76 two paragraphs below it**. The companies are named;
what is missing is the carve-out.

*This sentence read* **“no file anywhere records the provenance of that content”** *until the
review of 2026-09-11, and it was false.* `docs/decisions/0004_record_replay_cassettes.md`
§Consequences says it plainly: *“The repository carries a ~1.5 MB data artifact of third-party
responses, including raw posting HTML. That is the price of reproducibility.”* The repository
discloses the data and accepts the cost as a decision; what it does not do is the licence half.
**The sweep that reported none matched on `licen|copyright|provenance|verbatim|redistribut` and
ADR-0004 says `third-party`** — a zero from a reader that could not see its subject, which is
`SG-2`, in the same row that invokes `SG-2` twice against other people's guards. The finding
survives and is narrower: disclosed, unlicensed.

*What this is not, stated so a repair does not over-correct.* **No personal data.** A sweep of
all 1 845 050 characters of `http` and `extract` payloads for emails, LinkedIn profiles,
phone shapes and recruiter-contact wording returns **zero of each**, and the 326 `@` characters
are CSS at-rules in **302** cases; the other **24** are Twitter handles, npm scope names,
JSON-LD `@context`/`@type` keys and URI-parsing regexes, and not one is an address. *This read
as* **“CSS at-rules without exception”** *until 2026-09-11, written from a sample of twelve
contexts.* The sweep carries its own positive control — it counts
`reddit` 108 times and `Allegro` 76 — because a zero from a reader that never reached the
bytes is the shape `SG-2` is named for. Job ads are public marketing, the mechanism is
disclosed (`CLAUDE.md`:71 says the cassettes are committed; `README.md`:249 counts the eight
pages among the entries), and **deleting them is the wrong repair**: CI replays this cassette on
every push and the published table is a regression test over it. The cheap repair is a
provenance note that carves the recorded pages out of the MIT grant.

*`cv/candidate.md` claims to be synthetic and the claim was checked rather than taken*: zero
emails, phones, street tokens, Polish postcodes or eleven-digit runs in 4 208 characters, with
`P0w3r223` found 3 times as the control. `.env` is untracked and `.gitignore`:13 covers it;
`.env.example` carries two empty keys.

*`0010` §5's characterisation of the attack corpus reproduces.* `src/apply_scout/attack/` is 790
lines, its payloads a static tuple aimed at `.example` hosts and the link-local metadata
address, and `suite.py` substitutes `httpx.MockTransport` for the network and a function for
the model — *"no network and no key, by construction rather than by cassette"*. Nothing in it
adapts and nothing an outsider controls reaches it. The suite also names its own blind spot in
its docstring rather than leaving it to a reader.

*A near-miss worth recording, because it is `FG-1` and it nearly became a B finding.*
`README.md`:249 says the recording *"produced 68 entries"* and `eval/cassettes/eval.jsonl` holds
**106**. The figure is right and the file is right: the non-`llm` kinds sum to exactly 68 and
cost **$0.8802**, which is the README's `$0.88` to the cent, and the 38 `llm` entries arrived
later. *This named* **`5a3facc`** *until 2026-09-11, and that commit took the `llm` count from
0 to* **48** *over 116 entries; the 38 was set by* **`8dc7961`**, *which re-recorded the file to
106. The figure and the commit belonged to two different states of it.* A count taken off
`wc -l` would have recorded a
true sentence as false.

**A — `clear`.** **300 tests pass** in 6.05 s and `ruff check .` reports *All checks
passed!*; CI's last three runs are green, the newest 2026-09-09. Error handling is the strong
half: **zero bare `except`, zero `except Exception`, zero `pass`-only handlers** across `src/`.
One `Any` in the whole tree — `github.py`:123, `_get_json() -> Any | None`, which is parsed
JSON and is the place the annotation is honest rather than lazy. No `print` outside `cli.py`,
`__main__` and the report renderers. HTTP status literals are protocol constants, not the
hardcoded-threshold shape; the tunables live in `config.py`.

Measured with an AST walk rather than by reading: **ten functions exceed
`good-practices.md`'s fifty lines** — `agent.py:run` 138, `retrieval/report.py:markdown` 115,
`attack/report.py:markdown` 104, `evaluation.py:agent_assess_fn` 99, `pipeline.py:assess` 70,
and five between 52 and 57. `run` is the agent loop and reads as one job, but it inlines the
budget check, the continuation accumulator and trajectory recording in one body. Two files
pass the *typical* band without approaching the 800 ceiling: `cassette.py` 596,
`evaluation.py` 428.

*One observation, and it is the second occurrence of A-1's* — so it goes to §5 rather than
staying here. `tests/test_retrieval.py`:188
(`test_the_fast_path_agrees_with_matching_mentions`) puts its only assertion inside
`for query in queries`, so an empty fixture passes it silently. It is not vacuous today
because `:68` pins `(misses, len(queries)) == (63, 72)` and would redden first — but again
the protection lives in a different test from the one that names the property.

*Ten more tests share the shape and are not observations*, because each iterates a
module-level constant (`ARMS`, `PAYLOADS`, `pages.PLACEMENTS`, `UNSOURCEABLE`, `RETRIEVERS`)
or a helper that cannot return empty. Two defend themselves outright and are worth copying:
`test_docs_page.py`:917 iterates `zip(..., _root_blocks(), strict=True)`, where a missing
block raises instead of shortening the loop, and `_root_blocks()` asserts its own two
preconditions and is destructured as a pair at two call sites.

**B — `finding`. Three, and the strongest thing about this repository is the reason the
third one matters.** Every published figure reproduces: `eval/expected/pipeline.md`,
`agent.md`, `attack.md` and `retrieval.md` were each regenerated here — offline, no key, no
cost — and **all four diff byte-identical**. The replay reports *106 entries (1786 replayed,
0 recorded)*. The README's three table rows carry those values unchanged, and its
*63 of 72 probes* is a sentence `eval/expected/retrieval.md` prints itself.

**Three flags the CLI accepts and no document names**: `run --model`, `--max-steps`,
`--max-cost`. Read off `_build_parser()` and swept against `README.md`, `CLAUDE.md` and all
of `docs/`. Two are half-mitigated — `max_steps` and `max_cost` are documented as *concepts*
(`README.md`:37, `CLAUDE.md`:88), so a reader knows the budgets exist but not how to set
them; **`--model` has no mention in any spelling**, and a reader who has found `--models` on
`eval` will not guess the singular on `run`. This is A-1's `--min-success-failures` a second
time and goes to §5.

**`CLAUDE.md`:371 cites a path that resolves in a different repository and does not say so.**
`docs/adr/0004_what-carries-the-page-spec.md` is the index's; this repository has
`docs/decisions/` and **no `docs/adr/` at all**. Two sentences earlier the same paragraph
cites `docs/audit/0007_divergence-and-the-page-spec.md` *“in the private portfolio index”* — so
the correct form is demonstrated in the same breath as the incorrect one. Of **twenty path
citations over fourteen distinct paths** across `README.md`, `CLAUDE.md` and `docs/`, this is
the only one that fails; the other three that do not resolve literally are `0007` (correctly
qualified) and two `src/apply_scout/`-relative shorthands that are ordinary prose. *This read
as* **twenty distinct** *until 2026-09-11; twenty is the occurrence count and the reader that
produced it incremented per file, so a path cited twice counted twice.*

**The README's tables have no carrier, and here that is one `diff` away from being fixed.**
CI regenerates each table and diffs it against `eval/expected/*.md`; the README holds a
**hand-copied** second edition of the same numbers, and **nothing compares the two**. The
failure mode is not hypothetical: a metric change reddens CI until `expected` is updated, and
at that moment the README goes stale silently. They agree today — verified by replay, not by
reading. This is the portfolio-wide gap `0008` §5 records, but sharper: the artifact exists,
the guard exists, and only the copy sits outside it.

*Checked, and one of these was wrong*: of the eight CLI invocations the README prints, **the
four that carry flags parse against the real parser (:96, :99, :132, :235) and the other four
are refused** — `apply-scout run` in prose at :68 and :512, `apply-scout eval` in prose at
:129, and `apply-scout run` inside an `<img alt=…>` at :515 — because `run` declares `--url`,
`--cv` and `--github-user` `required=True` and `eval` declares `--tasks`. **None of the four is
a command the README offers a reader**, and the fourth is not prose at all, so the denominator
of eight was never eight runnable commands. *This read*
**all eight … zero refused** *until the review of 2026-09-11: the validator filtered to the
four containing `--` and the sentence quantified over all eight, which is the extractor's own
widening being credited to a check that never ran on the strings it added.* Those four are
prose references rather than runnable commands, so nothing on the page is wrong — but a
portfolio-wide argparse sweep built on *“a bare subcommand parses”* would pass everywhere for
the wrong reason. The section on the runner
comparison carries **its own erratum** for figures that outlived their recording, which is
this portfolio's own practice appearing in a submodule without being asked for.

**C — `clear`, and the checker is unusually quiet here.**
`python -m tools.pagespec --only apply-scout` reads **`clear, 3 undecided`**: every clause
`ok` or `n/a`, `contrast text` 22 of 22 measured with the worst at **5.17:1 against 4.5:1**,
**`contrast marks` no site**, and **`contrast
ground` 0 site(s) without a resolved ground**. The **three** `-` rows are `--border-control`
not declared *in each scheme* and clause 8 having no grouped figure — two causes, three rows,
all three admitted by their clause. *This said* **two** *until 2026-09-11, a hand count of an
instrument's output two lines above a paragraph corrected for the same thing.*

*The zero is shared, not unique, and this paragraph claimed otherwise.* It read
**“alone among the eight surfaces that report it”** until 2026-09-11. **Three surfaces read
`contrast ground` 0** — `apply-scout`, `mlops-car-price` and `pl-jobs-lora` — and all three
share the same profile exactly: `clear, 3 undecided`, `contrast marks` no site, ground 0.
Eight surfaces report a non-zero count, which is the set the struck phrase named and the set
`apply-scout` is not in. The verdict does not move; the superlative was never measured.

Read at a recruiter's pace, the first screen does its job: the eyebrow says what this is in
one line, and the `h1` — *“This agent's retriever finds the evidence for 8 of the 27
requirements a repository can prove”* — carries a figure, a denominator and a claim. It is
also the only headline in the portfolio that leads with the project's **own weakest number**,
which is a deliberate and defensible choice: the page's argument is that the one link nothing
scored was the one every other metric depended on. The attack section is the strongest writing
on any of the twelve — it publishes **`exfiltrate` → succeeded every time** in both arms,
explains why (*“an allowlist bounds where a request may go, not what it carries”*), and states
that every run first removes the guard and **requires** the attack to land before the table is
written. A positive control inside the artifact, which is what §3.6 asks of a guard.

*Three wordings proposed, all shorter or level, none generic — for a repair session, not for
this one.*

1. **The `40` tile is the weak one.** `40` / *attack attempts against the production toolset*
   is a bare count whose outcome sits four screens below, on a page whose own table says one
   payload class lands every time. A reader who stops at the tiles may take it either way.
   Proposed: **`4 of 5`** / *attack payload classes the harness stops across 40 attempts —
   exfiltration is not one*. Same space, carries the result and keeps the failure.
2. **`62%` has no denominator on the tile.** *of the task set produces a deliverable* →
   *of the 8-task set produces a deliverable*. Two characters.
3. **The sub-headline opens on an unresolved pronoun.** *“Nothing in the harness could see
   that.”* → *“Nothing in the harness could see those misses.”* One word, and the reader
   stops going back to the `h1` to find the referent.

**D — `finding`, and it is the issue tracker describing code that moved.** Hygiene is
otherwise the best in the portfolio: MIT detected by GitHub from `LICENSE`, **eighteen topics**,
homepage set to the Pages URL, a description carrying the same claim as the page, `main` the
only branch, CI green on its last three runs.

Five issues open, all from 2026-07-27, each read against the code:

| # | title | verdict | evidence |
|---|---|---|---|
| 3 | headless fetch for JS boards | **still real** | `git grep -ni 'playwright\|selenium\|headless'` over the tracked tree returns **one** hit, `README.md`:388, restating the limitation. *This cell cited `src/apply_scout.egg-info/PKG-INFO`, which `.gitignore`:4 excludes and no clone has: the sweep behind it was `grep -r`, the filesystem walk this portfolio's own rules forbid for exactly this reason* |
| 4 | search source, not just the README | **still real, and now quantified** | `tools/github_evidence.py`:46 is still `needle in readme.text.lower()` (*:41 until 2026-09-11 — that is `needle = requirement.strip().lower()`, five lines up; a citation that does not resolve, in the evidence column of a finding about citations that do not resolve*), no code-search call anywhere. The gap the issue argued in prose is the page's `h1` today: 8 of 27 |
| 5 | semantic requirement matching | **premise obsolete, proposal open** | the issue's subject `requirement_f1` **was deleted in `2090fcb`** and replaced by `requirement_coverage` (`evaluation.py`:93) under `ADR-0005`. Its *“~0.3 F1”* is a number the harness stopped producing; `README.md`:187 records the old 0.33 / 0.23. The embedding proposal is untouched |
| 6 | claim-level entailment guardrail | **still real** | `guardrail.py` carries `_is_grounded`, `requirement_grounding` and `evidence_grounding` — all provenance. Nothing checks entailment, and the README says so |
| 7 | grow the eval set to 20-30 | **still real** | `eval/tasks.json` holds **8** |

**The finding is #5, with #4 beside it.** A public tracker entry whose Context paragraph names
a function the repository deleted is a claim about the code that is false, and #4 cites
`src/apply_scout/github.py` for a function that now lives in
`src/apply_scout/tools/github_evidence.py`. Neither is expensive — an edited body each — and a
scan may not touch them, which is why they are written here.

**The cheapest observation that would falsify each `clear`.** For **A**: run the mutation
battery over `tests/test_retrieval.py` and see whether `:188` reddens on its own assertion or
on `:68`'s pin. For **C**: a `--fetch` run, which judges the served bytes — this scan read the
committed file, and `apply-scout` publishes through Pages from `docs/`.

**Not checked.** `docs/decisions/` holds twelve ADRs and this scan read four of them — **five
after the review, and the fifth is the one that falsified this row's E2 sentence.** For the
claims axis B needed; the rest are unread prose. The `llm` half of the cassette (38 entries,
$0.2950) was counted and characterised but its recorded model replies were not read. And the
retrieval judgment set (`eval/retrieval/judgments.json`, 695 lines) was replayed rather than
inspected — a wrong judgment reproduces exactly as well as a right one.

### A-3 — `it-job-radar`, session 3

Scanned 2026-09-14 at index `5664e43`, gitlink `1e65bfc`, entry state clean: index `HEAD`
identical to `origin/main`, twelve pointers matching, nothing uncommitted, no open portfolio
pull request. **Five axes**, E being E0 and E2's third-party half.

*Two things the record already said about this repository, and one of them is stale.* §2.2's
baseline lists it among the five reading `1 fail`; **§6's own warning row applies here** —
`ADR-0008` §10 took the marks census 88 → 26 and this surface went clean, so axis C quotes the
run this session made. And A-1 already measured `--seed 20260814` in this README and dismissed
it as a different shape, a literal a reader types rather than a value the code derives; it is
not re-raised.

**E0 — `finding` · metadata, and it is R-1's.** Three identities and no fourth:
`P0w3r223 <p0w3r2243@gmail.com>` 193 fields, GitHub's noreply 36, and
`Piotr Cząstkiewicz <p0w3r2243@gmail.com>` 9. **9 of 119** commits carry the real name,
reproducing R-1's table cell exactly by R-1's own method — counting commits, not fields. The
address is the portfolio's published contact and is not a finding.

**E2 — `finding` · third-party data, and it is a much narrower one than A-2's. Read that
sentence before the paragraph: this repository has done the work A-2's repair had to invent.**

The artifact is **published**, not merely committed: `docs/data/` holds ten Parquet files
served from GitHub Pages, 1.24 MB by the manifest's own count, and `docs/adr/0002` is a
policy deciding exactly what may be in them. It has already survived one audit correction —
the 2026-08-13 amendment replacing *"not resolvable back to a listing"* with pseudonymisation,
because the salt is committed and the source enumerates its own GUIDs.

*Verified rather than taken from the ADR.* Every one of the ten committed Parquets was read
and **not one carries a redacted or internal column** — `config.REDACTED_COLUMNS` is
`company`, `offer_url`, `title` and `INTERNAL_COLUMNS` is `raw_name`, `vacancy_key`; the
schemas hold none of them. The committed set equals `config.DATASET_TABLES` exactly, in both
directions. `sitemap_offers`, which `ADR-0002`'s own amendment names as the re-identification
vector, publishes hashed ids and dates and no URL or slug. `job_offers.db` is untracked and
`.gitignore`:15 covers it. `manifest.json` travels with the data and names the source, the
redacted columns, and the pseudonymisation caveat in the ADR's corrected wording.

**The finding is that the terms exist in three places and are carried by none, and that the
one file a redistributor opens says nothing.** `LICENSE` grants MIT over the tree with no
mention of `docs/data/`. The carve-out lives in `README.md`:168 — *"MIT — see LICENSE. Job
data © theprotocol.it (Grupa Pracuj) — collected respectfully for educational,
non-commercial use"* — in the page footer at `docs/index.html`:900, and in
`manifest.json`'s `source.attribution`. **MIT permits commercial use and that sentence
withholds it, and no file says which governs the Parquets.** A `git grep` over `tests/` for
the attribution returns only the collector's parser tests: **no guard holds any of the three
statements**, so all three can go silently — which is the shape the sibling one repository
over now has `tests/test_notice.py` for.

*What this is not, stated so a repair does not over-correct.* **No personal data**: the
`applying` block is dropped at parse time, company and title never reach a published file,
and the published rows answer market questions rather than listing questions — which the
manifest states in its own words. The repair is not a redaction change and not a deletion; it
is a pointer from `LICENSE` and a guard over the attribution, and `apply-scout` `78d9899` is
the worked example.

*One claim `ADR-0002` makes about the future was checked rather than assumed.* Its
Consequences say `docs/research/data-sources.md` *"should gain a short section pointing at
this ADR"*. It has one, at `:18`. Not a finding.

**A — `clear`.** **229 tests pass** in 28.9 s and `ruff check .` reports *All checks passed!*
Error handling is the strong half and it is not a near-miss: **zero bare `except`, zero
`except Exception`, zero `except BaseException`, zero `Any` annotations** across twenty
modules in `src/`.

*The two shapes a sweep flags here both resolve for the code, and both were read before being
written down.* `collect/theprotocol.py`:193 is a `pass` under `except requests.RequestException`
— not a swallowed error: `state` is initialised to `config.FETCH_FAILED` *before* the `try`
and the `finally` records the outcome into the frame, so a failure is written down and stays
eligible for retry, which is what the docstring four lines up says it does. And all **25**
`print` sites in `src/` are in one file, `pipeline.py`, which is the CLI
(`python -m it_job_radar.pipeline observe`). Neither is a finding.

Measured with an AST walk rather than by reading: **nine functions exceed
`good-practices.md`'s fifty lines** — `site/build.py:gather` 95, `quality.py:snapshot_metrics`
91, `site/charts.py:accumulation_chart` 88, `pipeline.py:collect_and_store` 71,
`site/build.py:_headline` 60, and four between 56 and 58. Two files pass the *typical* band
without approaching the 800 ceiling: `db.py` 482, `site/build.py` 438.

**Two observations, and they converge on the same guard — the most consequential one in the
repository.** `tests/test_export.py`:53 `test_identifying_columns_never_reach_the_artifact` is
what `ADR-0002` points at when it says redaction is *"covered by a test asserting the excluded
columns are absent from every published file — not left to reviewer vigilance."*

*First, it does not read a published file.* Its `dataset` fixture builds a two-offer synthetic
database and exports it to `tmp_path`, so it proves the **exporter** redacts. **Nothing asserts
the redaction of the bytes a reader downloads.** `tests/test_committed_dataset.py` is the only
test in the suite that opens `docs/data/` — and its own docstring is the sharpest statement of
the gap: *"Every other test in this suite builds a synthetic database and checks what `export`
writes from it. That leaves the files a reader actually downloads guarded by nothing."* That
file was written for a defect applied to the artifact after export, and its five tests cover
commit hashes, manifest agreement and the pyarrow that wrote each file. **Redaction is the one
property `ADR-0002` says is the reason the artifact may be published at all, and it is the
property that file does not check.** The sibling bytes-level test, `:78`, checks
`offers.parquet` alone rather than every published file, so the ADR's *"every published file"*
is true of the column check and not of the byte check. *This scan read all ten committed
Parquets and found no leak* — the observation is about the carrier, not a breach.

*Second, and it is `0010` §5's shape for the third time — with the weakest protection of the
three.* Every assertion in that test sits inside `for table in config.DATASET_TABLES`, so an
emptied tuple makes it pass over nothing. In `auth-log-scan` the property was held by a `len`
pin in a different test and in `apply-scout` by a `(misses, len(queries))` pin; here
**`DATASET_TABLES` is pinned by nothing at all** — `git grep` finds it in `config.py`:141 where
it is defined and in `test_export.py` twice, both times as the thing being iterated. What
stands between an emptied tuple and a green redaction test is `:62` reading
`offers.parquet` by literal name and failing on a missing file. That is incidental protection,
not a guard.

*Three more tests share the loop shape and are not observations*: `test_analytics.py`:81 and
`test_quality.py`:267 iterate a module constant whose docstring explains that reading config
rather than repeating it is the point, and `test_site.py`:162 calls
`build._assert_figures_carry_n(page)` outside its loop, which is the answer the other two
repositories had to be shown.

*A method note this scan owes the next one, because it nearly became a false finding.* §3.3
gives `pytest` for this repository, and a bare `pytest` in an environment without the package
installed produces **18 collection errors**, every one `ModuleNotFoundError: No module named
'it_job_radar'` — which reads exactly like §3.4's `blocked`. It is not: `pyproject.toml`
declares no `pythonpath`, `requirements.txt` is `-e .[dev]`, and CI installs with
`pip install -e .[dev] -c constraints.txt`. **The README's command is correct and the
environment was wrong.** Reading `requirements.txt` rather than assuming is what caught it;
the figures above come from `PYTHONPATH=src python -m pytest`, which changes no file.

**B — `finding`. Three, and two of them are shapes this audit already owns an instrument for.**

**The README states the published dataset as `~250 kB` and the artifact states itself as
1 244 431 bytes.** `README.md`:82 — *"`docs/data/` holds the artifact the page downloads
(~250 kB)"* — against `manifest.json`'s own `"bytes": 1244431`, which reproduces **to the byte**
as the sum of the ten committed Parquets. That is **1 217 kB, near five times the figure**, and
no reading rescues it: the largest single file is `offers.parquet` at 222 kB, and **the page
downloads no Parquet at all** — `docs/index.html` references `manifest.json` and nothing else,
because `ADR-0001` dropped DuckDB-WASM and the page is rendered server-side. The artifact
prints its own size, the README carries a hand-copied older one, and **nothing compares them**:
`git grep README -- tests/` returns no test that opens the file. *`README.md`:55's `241 kB` is
not this defect* — it quotes `ADR-0001`'s historical bundle comparison and reads as history.

**`verify --dataset` is accepted by the CLI and named in no document.** Third occurrence of
§5's flag shape, after `auth-log-scan`'s `--min-success-failures` and `apply-scout`'s three.

**`export --out` reads as documented only because a different subcommand's example contains
the string.** `--out` appears exactly once in nine markdown files —
`docs/plan/0001_implementation-walkthrough.md`:319, `pipeline site --out docs/` — so `site --out`
is documented and `export --out` is not. **This is `apply-scout`'s `--out` exactly, in a second
repository**, and it is worth saying how it was found: by the per-(subcommand, flag) sweep built
for `apply-scout` `78d9899` after a whole-corpus sweep had called that flag documented. The
instrument the last repair produced found its first new occurrence on its first outing. §5.

*Checked, and this repository passes where the sibling did not.* **Every markdown link target in
all nine documentation files resolves** — zero unresolved, measured by walking each `](…)` against
the file's own directory. The path-citation shape `0010` §5 records is not present here; nothing
*guards* it, which is the §5 entry's point, but there is nothing to repair.

*Also checked and reproducing.* `manifest.json`'s `coverage` gives `offers_listed` 6571,
`attributes_known` 6570, `share` 0.9998, and `README.md`:142 states *"6570 of 6571 listed
adverts (99.98%)"*. `duplicate_posting_share` 0.388 against `README.md`:39's *"38.8% of
adverts"*. Both exact.

**C — `finding`, and the checker cannot see it by construction.**

`python -m tools.pagespec --only it-job-radar` reads **`clear, 3 undecided`**, exit 0: `1
composited` 2 usages, `4 h1` unjudgeable, `contrast ground` 227 sites without a resolved
ground and 4 selectors it does not read. **No `contrast marks` row at all**, which means the
key is `ok` rather than undecided — `ADR-0008` §10's census change landed here. *§2.2's
baseline lists this surface among the five reading `1 fail` and §6's warning row is exactly
right: it is stale, and this paragraph quotes the run this session made.*

**`docs/index.html` prints `100.0%` for a figure the artifact states as `0.9998`.**
`site/build.py`:388 is `Kpi("Of the live market", f"{coverage['share']:.1%}", …)` and
`manifest.json`'s `coverage.share` is `0.9998` — so the tile is a **rounding**, which `0007`
§5.0 forbids in the same sentence that made clause 8 satisfiable. A reader of that tile is told
the snapshot covers the entire live market; it covers 6 570 of 6 571. **The index checker
cannot catch this** — it reads HTML and CSS and has no way to know the artifact's value, which
is `ADR-0004` §5's split working exactly as designed — and **this repository's own suite does
not pin the tile**: `git grep` over `tests/test_site.py` for the value or the coverage key
returns nothing. *It knows the class*: `tests/test_pairs.py`:137 is
`test_the_bar_states_a_lift_rather_than_rounding_it_into_a_count`. The sub-line directly beneath
prints *"6570 of 6571 listed today"*, so the honest figure is adjacent and the defect is a
headline that overstates what the line under it corrects — a finding, not a howler.

Read at a recruiter's pace the first screen does its job. The eyebrow dates the snapshot, the
`h1` is a claim with a result in it — *"Most junior IT offers in Poland are not development
jobs"* — and the sentence under it carries the denominator: *"97 of 368 vacancies open to
juniors are IT support and service-desk work … Development accounts for 72."* The eleven
section headings are questions rather than nouns, which is the strongest structural thing about
the page.

*One tile needs two readings, and the cause is one numeral meaning two things.* The salary tile
reads **`28%`** / *Disclose a salary* / *"of the rest, 28 published one we withheld as a unit
error"*. The headline `28` is a percentage and the `28` two lines below is a count of adverts,
with nothing between them saying so.

*Three wordings proposed, all shorter or level, none generic — for a repair session, not for
this one.*

1. **The coverage tile, which is also the clause repair.** `100.0%` / *Of the live market* →
   **`6 570 of 6 571`** / *Live market covered*. It prints the two integers the artifact
   already holds, so the rounding disappears rather than being made more precise, and the label
   finally says what the number is instead of what it is a share of.
2. **Disambiguate the salary sub-line.** *"of the rest, 28 published one we withheld as a unit
   error"* → *"of the rest, **28 adverts** published one we withheld as a unit error"*. Two
   words, and the tile stops using `28` for two quantities.
3. **`Of the live market` is a fragment that needs the tile above it to parse.** Every other
   label on the page is a noun phrase that stands alone — *Vacancies analysed*, *Thin strata*.
   Proposal 1 fixes this as a side effect; it is listed separately because the label is wrong
   even if the figure is left alone.

**The cheapest observation that would falsify the `clear` on axis A.** Empty
`config.DATASET_TABLES` and run `test_identifying_columns_never_reach_the_artifact`. If it
passes, the redaction guard is vacuous over the property `ADR-0002` calls the reason the
artifact may be published; if it fails, it fails on `:62`'s literal `offers.parquet` rather
than on its own assertion, which is the observation above stated as a measurement.

**D — `finding`: a decision this repository reversed, still advertised on its front door.**

Hygiene is otherwise clean and there is nothing else to report: MIT detected by GitHub from
`LICENSE`, homepage set to the Pages URL, **`main` the only branch**, **zero open issues**, and
the last three CI runs green.

**`ADR-0001` is not the defect — it is the model.** Its `Status` line reads *amended
2026-08-12*, and an Amendment section measures the WASM bundle at 21.1–37.5 MB raw against the
*"~3 MB"* the Decision had assumed, concluding in its own words: ***"The interactive layer is
dropped."*** The Decision paragraph stands as written under that Status line, which is this
portfolio's *record a correction rather than quietly fix it* practice working exactly as
intended.

**Three places downstream still state the dropped half as current fact.**

| where | what it says | why it is false |
|---|---|---|
| the GitHub **description** | *"…and browser-side DuckDB analytics over a published Parquet artifact"* | `docs/index.html` contains **zero** occurrences of `duckdb` or `wasm`; the page fetches `manifest.json` and no Parquet |
| the topic **`duckdb-wasm`** | one of fourteen | the same. `duckdb` alone is correct and stays — it is a real dependency (`duckdb>=1.1,<2`) and the build-time analytical engine |
| `src/it_job_radar/analytics/__init__.py`:8 | *"DuckDB is the analytical engine on both sides: here over Parquet on disk, **and in the browser over the same file**"* | in the source, where a reader trusts it most |

The description is the sharpest of the three because it is what a recruiter reads before opening
anything, and because `README.md`:53 already states the correction — *"dropped once the bundle
measured 21–37 MB"* — so the repository contradicts itself between its front door and its first
page. **Neither is expensive**: an edited description, one topic removed, two lines of docstring.

*One portfolio-level inconsistency, recorded as an observation and not as a finding against this
repository.* `pyproject.toml` declares **zero `keywords`** against fourteen topics. `apply-scout`'s
`CLAUDE.md` states the rule — *"`pyproject.toml`'s `keywords` lead; the GitHub topics copy them …
Every entry is backed by code"* — and **this repository's `CLAUDE.md` does not carry it**, so
nothing here is being violated. Which of the twelve state the rule is a §5 question a single
sweep answers, not a per-repository finding.

**The cheapest observation that would falsify each remaining verdict.** For **D**'s clean half:
`gh issue list --state all` rather than `--state open`, in case a closed issue describes code
that moved — the `apply-scout` D-2 shape, which an open-only listing cannot see. For **E2**'s
*no leak*: read the Parquet **row values** rather than the schemas, since a redacted column name
does not prove a company name is absent from a free-text field that survived under another name.

**Not checked.** `notebooks/01_analysis.ipynb` was counted and not executed. `docs/plan/0001`
(319+ lines) and `docs/ideas/0001` were opened only where a citation pointed into them, so their
claims are unread prose. The ten Parquets were read **by schema and by row count, never by
value** — which is the E2 observation above and is the one gap in this row that could hide a
finding rather than merely defer one. And `constraints.txt` was read for `duckdb` alone; the
other pins are unverified against anything.

### A-2 errata, 2026-09-11 — twenty corrections, in three rounds

*Placed after the row and not inside it.* The first edition put this heading between A-2's
D axis and its closing two paragraphs, so **Not checked** — which the scan prompt's closing
item 1 makes mandatory — fell under the errata heading instead of under the row. A-1 is the
template and keeps both closers inside.

Found by re-deriving every figure in this row against the instruments after it merged — the
practice `CLAUDE.md` states and this row had claimed to follow. Each correction is made where
its sentence lives, with the struck wording kept beside it.

| what it said | what is true | axis |
|---|---|---|
| *no file anywhere records the provenance* | `ADR-0004` §Consequences names the third-party data and accepts its cost; only the licence half is open | E |
| *eight `http` records* | **nine**, over eight distinct URLs, one page recorded twice | E |
| *1 818 808 characters* | right for all nine records; **1 088 196** is the distinct page content, the tryjeeves page being 730 612 of it | E |
| *the 326 `@` are CSS at-rules without exception* | **302** are; 24 are handles, npm scopes, JSON-LD keys and URI regexes, and none is an address | E |
| *alone among the eight surfaces that report it* | **three** surfaces read `contrast ground` 0, with identical profiles | C |
| *twenty distinct path citations* | twenty **occurrences** over **fourteen** distinct paths | B |

**Three of the six are one defect in the reader rather than six in the arithmetic**, and it is
already named. *No file anywhere*, *without exception* and *alone among* are universal
quantifiers written from partial reads: a five-term sweep pattern that omitted the term the
answer used, twelve sampled contexts out of 326, and one surface's row read without the other
eleven beside it. **`SG-2` is a zero from a reader that cannot see its subject** — and this row
invokes `SG-2` twice against other people's guards while committing it three times.

*No verdict moves.* E stays `finding` · third-party data on a narrower claim, C stays `clear`,
B stays `finding` with its three. What moved is that E2 is **disclosed and unlicensed** rather
than undisclosed, which is a different conversation to have with the owner.

**Round two, from a `code-review` pass over the merged commit.** Eight more, each reproduced
before it was written down here:

| what it said | what is true | axis |
|---|---|---|
| *six companies' pages* | six live pages from **five** companies; The Athletic and HHAeXchange appear only as 404 stubs and a provenance note must attribute nothing to them | E |
| *all eight CLI invocations parse, zero refused* | the four carrying flags parse; the four bare ones are **refused** for missing required arguments. The validator filtered to the four and the sentence quantified over eight | B |
| issue #3's evidence cites `PKG-INFO` | `.gitignore`:4 excludes it and no clone has it. `git grep` returns one hit, `README.md`:388. **The sweep was `grep -r`** | D |
| `tools/github_evidence.py`**:41** | **:46**; :41 is `needle = requirement.strip().lower()` | D |
| *the 38 `llm` entries arrived with `5a3facc`* | `5a3facc` took it 0 — **48** over 116 entries; **`8dc7961`** re-recorded to 106 and 38 | E |
| *the two `-` rows* | **three** — `--border-control` is reported once per scheme | C |
| *Four characters* | **two**; the insert is `8-` | C |
| `test_site.py` pinned at **`:237`** | **:240**; :237 is `palettes = _palettes(css)`. Wrong in **all three** places it appeared — A-1's body, A-1's falsifier, §5 — so cross-checking them could not catch it | A, §5 |

**Round three, from the same pass's gap sweep.** Six more, plus two structural:

| what it said | what is true | axis |
|---|---|---|
| *no company is named anywhere in the repository* | `README.md`:167 names both 404 companies, five ADRs and both `eval/` data files carry their task ids, and **this row's own control counts `reddit` 108 and `Allegro` 76**. The fourth universal quantifier, refuted two paragraphs from where it stood | E |
| *four are refused* naming three sites | four, and the fourth is an `<img alt=…>` at :515. None of the four is a command offered to a reader, so the denominator was never eight runnable commands | B |
| *Four axes* | **five**; §3.1 and §3.4 both say five and the row carries five. §3.2 retired half of **E2**, not an axis. Wrong in `A-1` too, and corrected there | all |
| §5's guard is *ten lines* | **28 plus two helpers** at `bfe4bf2`, 18 at `1d02f6f`. A hand-typed figure inside the bullet arguing that class of figure is the defect | §5 |
| two errata lines opened with `* ` at column 0 | GFM reads that as a list item interrupting a paragraph, so the struck wording rendered as a stray bullet with runaway emphasis — the mechanism by which a reader sees the old claim, broken. **Nothing in `tests/` parses markdown, so it would never have reddened** | — |
| the errata heading sat inside the row | it displaced **Not checked**, which the scan prompt makes mandatory, out from under `### A-2`. Moved below the row | — |

**Twenty corrections over three rounds, and the count of universal quantifiers is now four.**
*The heading said* **fourteen** *for one commit, which was round two's total carried into a
third round — the count of the errata going stale inside the errata. It is computed from the
table rather than typed: twenty rows.*
Every one of them — *no file anywhere*, *without exception*, *alone among*, *no company is
named anywhere* — was written from a partial read in a row that names `SG-2` twice. The pattern
is not arithmetic and no instrument catches it: **this row should not have carried an absolute** 
**claim at all**, having declared in its own *Not checked* that it read four ADRs of twelve.

**The `PKG-INFO` one is the worst of the twenty** and not because of the line: the sweep
behind it was `grep -r`, which reads the working filesystem including everything `.gitignore`
hides. This portfolio's own standing rule says to count with `git grep` and `git ls-files` for
exactly that reason. The verdict happened to survive; the method did not.

**And `:237` is a figure taken from the record rather than from the instrument.** It is `A-1`'s,
repeated here twice without being re-derived, in a row whose own standing rule forbids that —
`FG-2`. §5 names that pair as the cheapest falsifier of `A: clear`, so a session running the
battery would have mutated an assignment, seen nothing redden and inverted the finding. **All
three sites are corrected by this round**, `A-1`'s two included, because the figure was never
A-2's to repeat.

*And the row declared the gap that falsified it.* **Not checked** said four of twelve ADRs were
read, and an absolute claim was then written across the eight unread ones. Declaring a gap and
quantifying over it in the same row is worth recording as more than either half alone.

### A-2 repair, 2026-09-14 — E-2 and B-2 closed, D-2 part-closed

**Closed by `apply-scout` `84d14ae` (#38), index pointer bumped in the commit carrying this
line.** One repository plus a pointer bump, no new module or signature, and
`python -m tools.pagespec --only apply-scout` reads `clear, 3 undecided` identically before and
after — the page was never in scope. §3.5's first column, twice over.

**E-2.** `NOTICE` carves the recorded pages out of the MIT grant, names each URL with its
publisher and board, and marks the two 404 records as contributing no page content — the
attribution the row warned a repair must not get wrong. `LICENSE` is untouched: GitHub detects
the licence from it, and that detection is an axis-D asset worth more than an appended
paragraph. The cassettes are not deleted; CI replays them and the published table is a
regression test over them. **The note states no count at all**, because the lists are the
measurement and `tests/test_notice.py` derives both directions from `eval/cassettes/`.

**B-2.** All three halves. `tests/test_readme.py` compares the results table cell by cell in
both directions, binds each attack row to the payload `attack.md` names, and re-derives
`63 of 72` from the computed retrievers table — *not* from `retrieval.md`'s own sentence, which
is a string literal in `retrieval/report.py`, so two hand-typed copies agreeing would have
proved only that someone typed it twice. The undocumented flags are documented, the two
budgets gained the `help=` they never had, and `CLAUDE.md`:371's unqualified `docs/adr/`
citation is qualified.

**Erratum, 2026-09-14 — the flag count was wrong in A-2 and wrong again in the repair that
closed it.** A-2 said **three** undocumented flags and the first repair repeated it, into a
README sentence, a commit message, a pull request body and the paragraph above. It is
**four**. `--out` belongs to both subcommands and appeared in the pre-repair tree only as
`python -m apply_scout.retrieval --out` and `python -m apply_scout.attack --out` in
`CLAUDE.md` — two entirely different commands — so a sweep asking *is this flag string named
anywhere* called it documented while a reader of `apply-scout run --help` had nowhere to read
about it. **The instrument could not tell a subcommand from any other**, which is the same
class as the hand-count the standing rules forbid: a figure from a reader that cannot see its
subject. Closed by `apply-scout` `78d9899` (#39), where the guard is rescoped to a block that
names the subcommand, and `apply-scout eval --out` is documented.

**D-2 is part-closed and stays open, and the reason is a contradiction rather than a
judgement.** The two issues carry a correcting comment each, stating what the tree says:
`requirement_f1` deleted in `2090fcb` and replaced by `requirement_coverage` at
`evaluation.py:93`, and the needle living at `tools/github_evidence.py:46` rather than in
`github.py`. **The false sentences remain in the bodies**, because editing a body means reading
it and the repair prompt forbids a repair session from reading issue bodies at all. §6 carries
the row; what is left is an edited body each, and it needs either a scan session or an explicit
exemption.

**Seventeen mutations, all red on the guard that names them**, over a collected-green baseline,
each green again after reverting. **Nine were written with the guards and eight came from the
`code-reviewer` pass — and all eight were green when first aimed.** They share one shape, which
§5 now carries. The sharpest is that the README paragraph documenting the three flags names
`--max-tokens` in order to say it does not exist, which put the string into the guard's own
search scope and pre-approved the flag this project is likeliest to add next.

*One finding from that pass is deliberately not folded in.* This repair fixed one dead
documentation link by hand and added two more that nothing resolves. That is §5's, not this
row's — and §5 states it correctly where this sentence did not: it read *"while this index has
`tools/citations.py` doing exactly that for its own prose"*, and `citations.py` resolves
**section** references. It parses a link target only to attribute a `§N` to a document and
never asks whether the path exists. **Nothing anywhere in this portfolio, this index included,
resolves a markdown path citation in prose.** The index's `tests/test_spec.py` does resolve
paths, but only the clause registry's `repo:path::test` triples, which is a different
population. Two sentences of one document disagreeing about one instrument is the shape §3.4's
own erratum records, and this one was caught by re-reading the module rather than the sentence.

**Erratum, and it is this row's own figure.** A-2 states the cassettes hold **1 818 808
characters of raw job-board HTML**. It does not reproduce at the same gitlink `c7958eb`, under
any of four readings: the `html` and `error` payload strings sum to **1 801 326**,
`str(payload)` to **1 804 498**, the whole JSONL lines of the nine `http` records to
**1 821 238**, and `json.dumps(payload)` to **1 857 545**. The record count (nine), the
distinct-URL count (eight) and the publisher list all reproduce exactly, and no claim in the row
or in `NOTICE` rests on the character figure — which is why it is corrected here rather than
repaired. It is the twenty-first correction to a row whose errata round closed at twenty.

### A-3 repair, 2026-09-14 — E-3, B-3 and D-3's tree half closed, C-3 left open

**Closed by `it-job-radar` `8ae0d51` (#37), index pointer bumped in the commit carrying this
line.** One repository plus a pointer bump, no new module or signature, and
`python -m tools.pagespec --only it-job-radar` reads `clear, 3 undecided` identically before
and after, down to the three undecided lines — no page was touched. §3.5's first column.
Suite **229 → 242**, `ruff check .` clean, and **eighteen mutations, all red on the guard
that names them**.

**E-3.** `NOTICE` states one exception to the MIT grant — `docs/data/` — naming the
directory and not the files under it, because that list is `manifest.json`'s and is rewritten
on every export. `LICENSE` is untouched on A-2's precedent: GitHub detects the licence from
it and that detection is an axis-D asset.

The repair is smaller than A-2's, and the reason is the more useful half of it: **the
sentence was already one constant.** `config.ATTRIBUTION` is what `export` writes into the
manifest and what the template renders, so two of the three statements the scan found were
derived before this pass ever started. What was carried by nothing were the *committed*
copies — a manifest published before the constant moves goes on serving the old sentence
under a page rendering the new one — and the README's, which said the same thing with an em
dash where the constant has a comma. `tests/test_notice.py` holds all four to
`config.ATTRIBUTION` and the carve-out to `config.DATASET_DIR`.

**B-3.** All three. The README's `~250 kB` becomes the figure `pipeline export` prints,
**derived** from `manifest['bytes']` rather than pinned, so a re-export moves the README with
the data. `verify --dataset` and `export --out` are documented where their subcommand is, by
the per-(subcommand, flag) sweep `apply-scout` `78d9899` built — **with its unit made
smaller, which is what this repository adds to the instrument.** That guard scopes a flag to
the *block* naming its subcommand, which works where blocks name one subcommand each. This
README teaches all six in a single fenced block, so a block-scoped reader calls `export
--out` documented on the strength of the `site --out` line two rows below it. In a shell
transcript the line is the unit.

Repaired in the same sentence and not a separate finding: `docs/data/` was described as
*"the artifact the page downloads"*, which the row's own B evidence refutes — the page
fetches `manifest.json` and no Parquet.

**D-3, and the row's figure did not survive the sweep.** `tests/test_decisions.py` permits
the retired claim only where the retirement appears within two lines of it *and* names the
decision — the shape `ADR 0001` itself uses. Both vocabularies are the ADR's own and are
asserted against it, along with the premise above them: re-adopt the browser half and the
guard stops demanding loudly rather than silently enforcing a twice-reversed decision.
`docs/adr/`, `docs/plan/` and `docs/ideas/` are outside the sweep deliberately — they are
dated records, and a plan step later abandoned is supposed to still read as it was written.

The two sites that are not in the tree — the GitHub **description** and the topic
**`duckdb-wasm`** — are **not done**: they are outward-facing repository metadata rather than
a commit, and this session did not have the owner's instruction for them. The row stays open
for that half, on D-2's precedent.

**C-3 stays open, and §3.5 is why.** The repair is known and the scan wrote it down:
`6 570 of 6 571` / *Live market covered* in place of `100.0%` / *Of the live market*. It is a
published figure an artifact must be re-run to produce — `site/build.py` renders the tile and
CI's `drift` job diffs the committed page against a rebuild — which is §3.5's second column.
The repair prompt reaches the same answer from the other side: a rebuild reads `docs/data/`,
and a repair session does not read a repository's raw data.

**Erratum to A-3's D row, and it is the row's own figure.** The row reads *"Three places
downstream still state the dropped half as current fact"* and names the GitHub description,
the topic, and `analytics/__init__.py`:8. **The tree held four, and the row found one of
them.** Measured by running the guard this repair added against the pre-repair tree at
`1e65bfc` in a detached worktree, with `NOTICE` — which did not exist there — dropped from
its roots: five sites are reported, `pyproject.toml`:19, `analytics/__init__.py`:8,
`analytics/engine.py`:8, `analytics/engine.py`:27 and `export.py`:10. Four state the retired
claim; the fifth, `engine.py`:27, is a true sentence about a reader inspecting the page's SQL
that matches the vocabulary, and it was reworded rather than counted. **Two of the four cite
`ADR 0001` while contradicting it**, and `export.py` justifies the choice of Parquet by a
capability nobody ships. Nothing in the row rests on the figure being three, which is why it
is corrected here rather than repaired.

*Why a scan would have had to be lucky to find all four.* `git grep` is line-based, and
`analytics/__init__.py`'s claim wraps: *"and in the"* ends line 8 and *"browser over the same
file"* opens line 9, so the string `the browser` is in neither. The same sweep at the same
commit returns six lines and **the one the row actually names is not among them** — it was
found by reading. The guard folds each line with the next for exactly this, and that is not a
hypothetical: it is how the row's own site behaves.

## 5. Cross-cutting

What recurred rather than happened once. A per-repository split cannot see a pattern by
construction; this section and §2's baselines are where patterns accumulate.

- **§2.3, E1 across all thirteen: clean.** Sweeping once rather than thirteen times is what
  made the three matches cheap to read together and dismiss together.
- **A flag the CLI accepts and no document names — three repositories, three sessions, and
  the shape has a second half nobody had measured.** `auth-log-scan`'s
  `--min-success-failures` (A-1), `apply-scout`'s `run --model`, `--max-steps`, `--max-cost`
  (B-2), and `it-job-radar`'s `verify --dataset` (B-3). **The second half is a flag documented
  under the wrong subcommand**, which a whole-corpus sweep reports as documented: `apply-scout`'s
  `--out` read as named on the strength of two `python -m apply_scout.retrieval --out` lines, and
  `it-job-radar`'s `export --out` reads as named because `pipeline site --out docs/` appears once
  in a plan document. **Two occurrences in two repositories, and the second was found by the
  instrument the first one's repair built** — the per-(subcommand, flag) sweep in `apply-scout`
  `78d9899`, on its first outing against another tree. That is the argument for the
  portfolio-wide sweep this bullet already asks for, now with a specification: ask per
  (subcommand, flag), against documentation blocks, never against the concatenated corpus.
  **The specification took two corrections on its first port, and both are about scope rather
  than about flags.** *The block is not always the unit*: `it-job-radar`'s README teaches all
  six subcommands inside one fenced block, so a block-scoped reader calls `export --out`
  documented on the strength of the `site --out` line two rows below it. In a shell
  transcript the line is the unit, and the sibling's blocks only worked because they name one
  subcommand each. *And the corpus is not every markdown file*: the first edition swept
  `docs/**/*.md` and went green over a deleted README line, carried by
  `docs/plan/0001`:319 — **the very line this bullet cites as the original false positive.**
  A 2026-08 implementation walkthrough documents nothing for a reader running `--help` today.
  So the specification is now: per (subcommand, flag), scoped to the line inside a fence and
  the paragraph outside it, over the documents that *teach* the CLI and not the ones that
  record what was once planned for it. Both were found the same way — read the parser, sweep
  the docs — and neither repository had any guard that could. `auth-log-scan` now has one
  (`tests/test_readme.py`, `bfe4bf2`), and it is **28 lines plus two helpers** — 18 when it
  landed at `1d02f6f`, grown because the first edition filtered on `startswith("--")` while its
  name promised every flag, so a short-only `-m` passed it silently. *This said* **ten lines**
  *until 2026-09-11, a hand-typed figure inside the bullet arguing that class of figure is the
  defect.* **Two occurrences make this the
  first shape worth a portfolio-wide sweep rather than a per-repository finding**, and the
  sweep is cheap: every repository with an `argparse` parser can be asked the same question
  without being scanned.
- **A guard whose every assertion sits inside a loop, protected by a pin in a different
  test.** `auth-log-scan`'s `tests/test_site.py`:263 against `:240`'s `len(bands) == 2`, and
  `apply-scout`'s `tests/test_retrieval.py`:188 against `:68`'s
  `(misses, len(queries)) == (63, 72)`. Neither is vacuous today and both would read as
  *caught* in a mutation battery while the guard that names the property proved nothing —
  `SG-1` at one remove, now twice. `apply-scout` also shows the answer: `test_docs_page.py`:917
  iterates `zip(..., _root_blocks(), strict=True)`, where a short iterable raises instead of
  shortening the loop.
- **The published figure and the artifact that proves it are one `diff` apart, and nobody
  takes the step.** `apply-scout` regenerates four tables in CI and diffs each against
  `eval/expected/*.md`, then hand-copies the numbers into `README.md` where nothing compares
  them; `auth-log-scan` quoted a terminal block no test read until this week. This is
  `0008` §5's carried README row meeting the audit from the other side: the row says no
  carrier exists, and what session 2 adds is that in at least one repository **the carrier
  already exists and the README simply sits outside it**.
- **A decision the repository reversed, still stated as fact by everything downstream of the
  document that reversed it.** `it-job-radar`'s `ADR-0001` dropped DuckDB-WASM, recorded the
  measurement that killed it, and says *"The interactive layer is dropped"* — and the GitHub
  description, one of fourteen topics, and a package docstring in `src/` all still advertise
  browser-side DuckDB. First occurrence, so it is here as a shape to watch rather than a rule:
  **an amended ADR is a fan-out, and this audit has so far only ever checked the ADR.** The
  cheap sweep is the inverse of the one the audit already runs — take each `Status: amended` or
  superseded decision in a repository and grep the tree and the GitHub metadata for the claim it
  retired. `0010` §4 A-3's D axis is the worked instance, and the same session found `apply-scout`
  D-2's issue bodies by the same question asked of a tracker instead of an ADR.
  **The repair measured the fan-out and the scan's figure did not survive it: three named,
  four in the tree, and the one the row named was the one a `git grep` cannot see** — the
  claim wraps, so `the browser` is in neither of its lines. So the sweep this bullet asks for
  is not a grep. `it-job-radar` `tests/test_decisions.py` is the first instrument for it:
  fold each line with the next, permit the claim only where the retirement sits within two
  lines *and* names the decision, and take both vocabularies from the ADR and assert them
  against it. It also states the premise, which is the half worth copying — re-adopt the
  retired design and the guard stops demanding rather than enforcing a twice-reversed
  decision. The exclusions are the other half: a dated record is supposed to still read as it
  was written, so `docs/adr|plan|ideas|research` are outside the sweep and the *manuals* are
  inside it.
- **Two repositories carry a deliberate attack corpus** — `apply-scout/src/apply_scout/attack/`
  and `doc-extract/results/attack-*/`. Both are self-authored, non-adaptive, and versioned;
  neither is content an outsider controls. Sessions 2 and 5 will read them, which is why
  those sessions are scans and cannot act.
- **A guard written against hand-maintained lists, keeping a hand-maintained list of its own.**
  Repair 1's guards did not show it; repair 2's did, **four times in one commit**, and every
  one was found by the `code-reviewer` pass rather than by the mutation battery — because a
  battery aims at the property a guard names and this defect lives in what the guard cannot
  see. `tests/test_notice.py` pinned its two cassettes by name three lines under a comment
  saying a guard reading one cassette would miss a page; `tests/test_readme.py` pinned two
  artifact files by name, keyed five attack rows on a column two of them share, and let
  `--max-tokens` through because the README sentence *denying that flag exists* put the string
  in its search scope. **The test for it is one line of derivation each** — a `glob` against
  the directory, a set comparison against the artifact — and the shape is worth a sweep of
  every guard this audit has added or will add, not a per-repository finding. It also
  generalises the observation above it: a registry inside a guard is the loop-with-one-assertion
  problem moved up a level, where the vacuity is structural rather than accidental.
  **The shape recurred inside its own repair, which is what promotes it from an observation to
  a rule.** The commit fixing those four opened with the sentence *"every registry below is
  asserted against the directory or the artifact it stands for"* and shipped three that were
  not: `DOCUMENTED_AS_ABSENT` pinned in one direction only, `BOARD_BY_HOST` with no used-entry
  check, and — the one worth the entry — a test **named**
  `test_every_approved_artifact_is_claimed_by_a_guard_in_this_file` whose body compared a
  directory to a constant and passed with every guard in the file deleted. A second review
  found all three. So the rule is not *derive your registries*; it is that **a registry must be
  answerable in both directions to something outside the file**, and the test asserting that
  is itself the one most likely to be written as a restatement. Closed at `apply-scout`
  `78d9899` (#39), where the artifact test runs the guards and records what they open —
  a source-text heuristic was tried first and convicted the two artifacts read *through* a
  registry rather than by literal, punishing the better pattern.
- **A figure from a reader that cannot see its subject, twice in one repair.** Distinct from the
  hand-count the standing rules already forbid: here an instrument ran, printed a number, and
  the number was wrong because the reader's granularity was not the claim's. A-2's *three
  undocumented flags* was per **flag string** where the claim is per **(subcommand, flag)** —
  `--out` read as documented on the strength of two `python -m apply_scout.retrieval --out`
  lines. And a `grep` measuring committed line endings matched every line of every file it was
  pointed at, so two docstrings shipped saying the blobs are CRLF when every blob in that
  repository is LF; **the tell in both cases was that the figure equalled a total that was
  lying around** — the file's line count, the corpus's flag count. Worth a habit rather than a
  guard: when a sweep returns a round or familiar number, mutate its input and check the number
  moves before quoting it.
- **A guard that sweeps a scope wider than the claim it makes, which is the registry shape
  one level up again — and the battery cannot see this one either.** Repair 2 found a guard
  keeping a hand-maintained list of its own; repair 3 found four guards whose *unit* was
  bigger than the property they asserted, and every one of them passed over the defect it was
  written for. The carve-out guard asked whether `NOTICE` names `docs/data/` **anywhere in
  the file**, and a mutation pointing the exception at `docs/dataset/` stayed green because a
  later paragraph mentions the right directory in passing; narrowed to the paragraph it
  stayed green again, because the next sentence says the file list is
  `docs/data/manifest.json`'s job. A carve-out is a sentence. The flag sweep read every
  markdown file rather than the manuals, and the retirement exemption read a whole TOML table
  rather than the claim's neighbours, so one `dropped` in a dependency comment excused the
  package `description` twelve lines above it — **a site the audit row had named.**
  **What separates this from the registry shape is who can find it.** A mutation battery aims
  at the property a guard names, and mutating a site *inside* the swept scope reddens whether
  the scope is right or not; only a mutation at the scope's edge says anything, and nothing
  tells you where that edge is except reading the guard. Two of the four were found by the
  `code-reviewer` pass, which is the second time that pass has caught a class the battery
  structurally cannot — `0010` §4 A-2's repair is the first. The other two the battery did
  find, by luck: the mutation happened to land outside. So the rule is not *write a smaller
  unit*; it is that **a guard's scope is a claim too, and it is the one no battery asserts** —
  state it in the docstring, and check it against the sentence the guard's name makes.

- **A repository's own prose cites paths, and nothing in any submodule resolves them.**
  `apply-scout`'s `CLAUDE.md`:371 cited `docs/adr/0004_…`, which exists in this index and not
  there — found by a scan, fixed by hand in repair 2, **which then added two more unguarded
  references in the same commit**. This index has carried `tools/citations.py` since
  `ADR-0009` §3 step 1 and gates on an unresolved `§N`; the twelve have nothing equivalent for
  either sections or paths. Second occurrence of a citation that does not resolve in this
  repository alone, and the first was in the evidence column of a finding about citations that
  do not resolve. **Cheap to sweep and not cheap to carry**: a per-repository link checker is
  twelve new guards, so the decision of whether it belongs here or there is `architect`'s.
  **Third occurrence, in a third repository, and the same ADR number.** `it-job-radar`'s
  `CLAUDE.md`:123 cited `docs/adr/0004_what-carries-the-page-spec.md`; `docs/adr/0004` there
  is `0004_analysis-population.md`, and the file it meant lives in this index. Qualified by
  hand in repair 3 and still carried by nothing. What the third occurrence adds is that it
  was **not found by the scan of that repository** — A-3's B axis measured every markdown
  link target in all nine `docs/` files and reported zero unresolved, which was true and
  scoped: `CLAUDE.md` is not in `docs/`. It surfaced in the `code-reviewer` pass over the
  repair, from a reader who happened to open the paragraph. Three repositories, three
  sessions, and not one of the three found by an instrument.

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
| 2026-09-14 | **v2.0**, repair | the prompt forbids a repair session to read issue bodies and sends a row it cannot act on any other way: `0010` D-2's repair *is* an edit to the bodies of issues #4 and #5. Its own remedy — *"send it back to a scan session rather than reading around it"* — cannot apply either, because a scan session may read them and may not act | **A correcting comment closes what a comment can close, and the row stays open for the body edit.** Repair 2 took that route with the owner's go-ahead: both issues now carry a comment stating what the tree says, written from the row and from `git`, with no body read. The body edit needs an explicit exemption or a scan/repair pair whose split this case does not fit. *Recorded rather than resolved: the rule is a guard, and reasoning about its intent to get past it is the practice `CLAUDE.md` forbids by name* |
| 2026-09-14 | **v3.0**, scan | §3.3 gives `pytest` for the nine repositories in its *the rest* row, and for `it-job-radar` a bare `pytest` in an environment without the package installed produces **18 collection errors**, every one `ModuleNotFoundError` — which reads exactly like §3.4's `blocked` and would have sent a clean repository back to the queue | **An import error is an environment verdict, not a repository one, until the repository's own install path is read.** `pyproject.toml` declares no `pythonpath`, `requirements.txt` is `-e .[dev]`, and CI installs before running — so the README's command is correct. Run `PYTHONPATH=src python -m pytest`, which changes no file, or install as CI does; and say in the row which was used. *Nearly written up as a finding in session 3; what caught it was reading `requirements.txt` rather than assuming* |
| 2026-09-11 | **v3.0** | the prompt names no sweep tool for axes B and D — its only `git grep` mention is about E0 — and session 2 swept axis D with `grep -r`, citing `src/apply_scout.egg-info/PKG-INFO` as evidence. `.gitignore`:4 excludes it and no clone has it | **Sweep tracked files.** `git grep` and `git ls-files`, never `grep -r` or a filesystem walk: `.egg-info/`, `eval/results/`, `reports/site/` and `.claude/sessions/` are all gitignored somewhere in this portfolio and all read as repository content to a walk. `0010` A-2's errata records the one cell it already cost |
| 2026-09-10 | **v2.0**, as a warning and not a contradiction | §2.2's surface baseline was measured at `2cb5d45`, about an hour before S14b gave `contrast marks` a verdict; a session quoting it would write `clear` into a row where its own run prints `1 fail`, with the `undecided` counts moved too | §2.2's erratum — axis C quotes the run the session made, and the key is `report-only`, which is why the gate still exits 0. **No count is given here on purpose**: this cell said *five of the eleven* until 2026-09-11 and was stale within hours of being written, because `ADR-0008` §10 took the marks census 88 → 26 the same evening and `it-job-radar` went clean. A warning about what a session's own run prints must not carry a figure the session's own run contradicts |
