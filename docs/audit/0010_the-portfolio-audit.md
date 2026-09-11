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
| 2 | `apply-scout` | `5278b1b` | `finding` · metadata (R-1) · third-party data | `clear` | `finding` | `clear` | `finding` | E-2, B-2, D-2 | four ADRs, the `llm` cassette half, the judgment set |

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

### A-2 — `apply-scout`, session 2

Scanned 2026-09-11 at index `5278b1b`, gitlink `c7958eb`, entry state clean and `HEAD`
identical to `origin/main`. Four axes, E being E0 and E2's third-party half.

**E0 — `finding` · metadata, and it is R-1's.** Three identities in the history and no
fourth: `P0w3r223 <p0w3r2243@gmail.com>`, `Piotr Cząstkiewicz <p0w3r2243@gmail.com>` and
GitHub's noreply. **13 of 116** commits carry the real name, which reproduces R-1's table cell
exactly. The address is the portfolio's published contact and is not a finding.

**E2 — `finding` · third-party data. The repository redistributes six companies' pages
verbatim under a blanket MIT notice.** `eval/cassettes/` commits **1 818 808 characters of
raw job-board HTML** across eight `http` records — six live pages and two `{"error": "HTTP
404"}` — from **Allegro** (two postings, SmartRecruiters), **tryjeeves** and **The Athletic**
and **HHAeXchange** (Lever), **Zapier** (Ashby), **KONUX** and **Reddit** (Greenhouse). `LICENSE`
reads *MIT / Copyright (c) 2026 Piotr Cząstkiewicz* over the whole tree, and **no file anywhere
records the provenance of that content or excludes it from the grant** — swept `README.md`,
`CLAUDE.md`, `docs/` and `eval/` for a licence, copyright or provenance note and found none
touching the recorded pages.

*What this is not, stated so a repair does not over-correct.* **No personal data.** A sweep of
all 1 845 050 characters of `http` and `extract` payloads for emails, LinkedIn profiles,
phone shapes and recruiter-contact wording returns **zero of each**, and the 326 `@` characters
are CSS at-rules without exception. The sweep carries its own positive control — it counts
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
later with `5a3facc`, *scoring the agent loop*. A count taken off `wc -l` would have recorded a
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
the correct form is demonstrated in the same breath as the incorrect one. Of twenty distinct
path citations across `README.md`, `CLAUDE.md` and `docs/`, this is the only one that fails;
the other three that do not resolve literally are `0007` (correctly qualified) and two
`src/apply_scout/`-relative shorthands that are ordinary prose.

**The README's tables have no carrier, and here that is one `diff` away from being fixed.**
CI regenerates each table and diffs it against `eval/expected/*.md`; the README holds a
**hand-copied** second edition of the same numbers, and **nothing compares the two**. The
failure mode is not hypothetical: a metric change reddens CI until `expected` is updated, and
at that moment the README goes stale silently. They agree today — verified by replay, not by
reading. This is the portfolio-wide gap `0008` §5 records, but sharper: the artifact exists,
the guard exists, and only the copy sits outside it.

*Checked and holding, recorded because a later reader should not re-derive them*: all eight
CLI invocations the README prints parse against the real parser (four carry flags; zero
refused, after the extractor was widened — its first version found three of eight, and a
zero from a reader that cannot see its subject is `SG-2`). The section on the runner
comparison carries **its own erratum** for figures that outlived their recording, which is
this portfolio's own practice appearing in a submodule without being asked for.

**C — `clear`, and the checker is unusually quiet here.**
`python -m tools.pagespec --only apply-scout` reads **`clear, 3 undecided`**: every clause
`ok` or `n/a`, `contrast text` 22 of 22 measured with the worst at **5.17:1 against 4.5:1**,
**`contrast marks` no site**, and — alone among the eight surfaces that report it — **`contrast
ground` 0 site(s) without a resolved ground**. The two `-` rows are `--border-control` not
declared and clause 8 having no grouped figure, both of which the clause admits.

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
   *of the 8-task set produces a deliverable*. Four characters.
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
| 3 | headless fetch for JS boards | **still real** | no `playwright`/`selenium`/`headless` in `src/` or `pyproject.toml`; the only match is `PKG-INFO` restating the limitation |
| 4 | search source, not just the README | **still real, and now quantified** | `tools/github_evidence.py`:41 is still `needle in readme.text.lower()`, no code-search call anywhere. The gap the issue argued in prose is the page's `h1` today: 8 of 27 |
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

**Not checked.** `docs/decisions/` holds twelve ADRs and this scan read four of them, for the
claims axis B needed; the rest are unread prose. The `llm` half of the cassette (38 entries,
$0.2950) was counted and characterised but its recorded model replies were not read. And the
retrieval judgment set (`eval/retrieval/judgments.json`, 695 lines) was replayed rather than
inspected — a wrong judgment reproduces exactly as well as a right one.

## 5. Cross-cutting

What recurred rather than happened once. A per-repository split cannot see a pattern by
construction; this section and §2's baselines are where patterns accumulate.

- **§2.3, E1 across all thirteen: clean.** Sweeping once rather than thirteen times is what
  made the three matches cheap to read together and dismiss together.
- **A flag the CLI accepts and no document names, twice in two sessions.**
  `auth-log-scan`'s `--min-success-failures` (A-1) and `apply-scout`'s `run --model`,
  `--max-steps`, `--max-cost` (B-2). Both were found the same way — read the parser, sweep
  the docs — and neither repository had any guard that could. `auth-log-scan` now has one
  (`tests/test_readme.py`, `1d02f6f`) and it is ten lines. **Two occurrences make this the
  first shape worth a portfolio-wide sweep rather than a per-repository finding**, and the
  sweep is cheap: every repository with an `argparse` parser can be asked the same question
  without being scanned.
- **A guard whose every assertion sits inside a loop, protected by a pin in a different
  test.** `auth-log-scan`'s `tests/test_site.py`:263 against `:237`'s `len(bands) == 2`, and
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
