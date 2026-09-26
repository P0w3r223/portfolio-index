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

Index `a9c3912` on `main`, level with origin, twelve pointers matching their own
`origin/main`, nothing uncommitted, no open portfolio pull request. S14a closed the same day
(`860ca48`, `a0d19cb` #32, `d440ab0` #10, `a9c3912` #115); S14b remains open.

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

*The second sentence is true of the portfolio as it has committed since a date between
2026-08-14 and 2026-09-03 and false of everything before it, where all thirteen repositories
merged their pull requests — 24 such commits on this index's own `main`. The figure above stands:
it was measured against `refs/pull/*`, which holds the heads whether the merge squashed them or
not. §6's row of 2026-09-18 and A-6's errata are the correction; this note is here because §2 is
the state the audit was opened against and is corrected rather than rewritten.*

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
what it says.** §2 is frozen by `ADR-0004` §5 and stays as measured — but S14b (`bcd53db`,
`#117`) gave `contrast marks` a verdict, and at that commit **five of the eleven read
`1 fail`**: `ab-lab`, `auth-log-scan`, `car-price-ml`, `it-job-radar`, `pl-review-sense`. The
run still exits 0 because the key is `report-only`, and the reason is printed under
`gate policy` on every run. **The `undecided` counts moved with the verdict and the whole
sentence above is stale, not half of it**: `ab-lab` reads 2, the other ten read 3, and
`wroclaw` under `--fetch` reads 4 — not the 4-or-5 and 5 the line records. So a scan
session's axis C compares its own `--only` output against the checker in front of it, never
against this line; the number a row quotes comes from the run it made. Verified 2026-09-10 at
`bcd53db`: 619 tests green, gate 0, 153 marks below 3.0:1 of 739 measured, and `--fetch`
reports no `served` mismatch on any of the twelve.

**The two censuses below are not stale, and the reason is worth stating because checking it
misleads.** Both reproduce byte-for-byte at `bcd53db` — S14b moved neither. But this
paragraph has just quoted a `--fetch` figure for `wroclaw` inside a block whose header names
the *fetchless* run, and a reader who reaches for `--fetch` to check it sees `portfolio 98`
and `--border 69` against the bullets' 95 and 60. That is the twelfth surface joining the
census, not three more moved figures: `--fetch` judges all twelve, and §2.2's own header
names `--detail` without it for exactly that reason. Found by the review of this erratum,
which walked into it.

*The gap is 54–70 minutes — `a9c3912` merged 13:05, `1b97805` wrote this section 13:21,
`bcd53db` merged 14:15. The first version of this erratum said "hours", twice, in a
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
| 13 | **this repository** — `tools/`, `tests/`, `docs/`, **and the tracked files at the root** | scan |
| 13b | `P0w3r223/P0w3r223` — the profile README | scan |
| 13c | `infra-docker`, `infra-docker-powiadomienia-teams`, `infra-docker-workmate`, `student-wellbeing-pwr` | secrets only |
| R1…Rn | repair sessions, driven by §4 | repair |

*Session 13's row gained its root clause 2026-09-10: `pyproject.toml`, `.gitignore` and the
workflow are tracked, are this repository's, and fell outside all three named directories. The
audit repairs that class of disagreement elsewhere, and had just created one of its own. The
clause named a fourth file, the identifier template, which was deleted 2026-09-11 with §3.2.*

***Session 13's subject changed repository on 2026-09-17, and the denominator did not.*** The
row read `current_projects` until then. `0011` §6 route A published this index as
`P0w3r223/portfolio-index` and left `current_projects` private as the archive, so session 13
scans **this** repository — the one holding the checker the audit's axis C runs. The archive is
deliberately **outside the corpus and outside the queue**: its audit of record is `0011`, which
read every blob in its object database and 533 commits across every ref including `refs/pull/*`,
which is a stronger answer on axes E0 and E1 than a scan session could reach, and nothing in it
will change again. **Fifteen sessions, not sixteen.** *The alternative considered and refused was
a session 13d for the archive: it would have re-asked with a weaker instrument the questions
`0011` had already closed, and §3.4 would then have owed a verdict on a repository no repair can
touch.* §2.1's corpus row still names the archive and still holds its figures, because §2 is the
state this audit was **opened** against and re-measuring it would be the practice §4's header
refuses; `0012` §3 is where that is recorded rather than patched.

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
| the index itself | none | full `pagespec --detail`, which is the census run | `pytest` |
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

**Since 2026-09-18 the `Open` column is a vocabulary rather than prose**, and the argument for
it is this document's own first rule. *What next* was answered by reading 2 800 lines and
counting by hand, in a repository whose standing rule is that a figure comes from an instrument
and whose three hand counts of one population read 15, 18 and 19 against a true 20.
`python -m tools.queue` reads this column now. Each item is a row id, one state word, and
`·` between items:

- `open` — raised, not acted on, and actionable by a repair session today.
- `closed` — acted on, with the commit **on `main`** in the row body. *Amended 2026-09-18 by
  the first closure that has none*: where the repair changes no file — an issue closed, a
  repository's metadata moved — the row body cites the **outward artefact a reader can
  resolve** instead, and says why there is no commit. `D-6` is that case whole, and `D-3` was
  half of one on 2026-09-14. The clause is here rather than in the row because a definition a
  row quietly departs from is a definition that stops being read.
- `declined` — deliberately not repaired, the reason in the row body. Without this state a
  refusal and a backlog item are the same cell, and a queue that cannot say *no* grows a
  ceiling no reader can see.
- `deferred` — nothing a session may do closes it: it waits on a decision the owner owns
  (`R-1`), or on a capability neither session type has — `C-3`, whose repair would have a
  repair session read the raw data it may not, and `D-2`, which is that rule in the mirror.
- `pending` — the repair exists and is not on `main` yet: an open pull request, or a pointer
  not bumped. `tests/test_queue.py` exempts it from the ancestor check, which is the whole
  reason the state is named.

*`declined` and `pending` have no instance today.* Declaring them ahead of the first one is
deliberate: both are produced by work already scheduled, and adding a state on the day it
arrives moves the parser, both prompts and this paragraph inside a commit busy being about
something else.

**The ids are not a uniform scheme and this column does not pretend otherwise.** `A-4` names
row 4 *and* that row's A-axis finding, because the row heading took the letter first; rows 5
and 6 work around it in prose, and §5 writes “(C in A-5)” and “(B in A-6)” for
exactly that reason. **Four findings had no address at all and were given one on 2026-09-18**
— `C-4`, `C-5`, `C-6`, `D-6` — because a column cannot index what has no id. No verdict
moved and nothing was renumbered: repairing the `A-N` collision would move 25 sites for `A-4`
alone, and this record has already paid once for an identifier renumbering, in A-4's errata,
where five ids collided with a scheme in which `B-2` was taken.

**An id addresses a paragraph by convention, and the convention is written down here rather
than stamped onto six rows.** `<axis>-<session>` is the axis paragraph under that session's row
heading — `C-6` is *“**C — `finding`, and it is the first surface I have scanned that the
checker fails**”* under `### A-6`. A suffixed id — `B-4a`, `E-5c` — is a labelled paragraph and
carries its literal, because a sub-finding has no axis heading to sit under. *The alternative was
to stamp the four new ids onto their paragraphs; it was refused because the other rows' axis
paragraphs carry no literal either, and a document with two notations for one address is the
defect this paragraph is already about.* Reported by the review of this stage, which grepped
`C-6` and found the announcement and the cell.

| # | Repo | Index SHA | E | A | B | C | D | Open | Not checked |
|---|------|-----------|---|---|---|---|---|------|-------------|
| — | *portfolio-wide* | `a9c3912` | `finding` · metadata | — | — | — | — | R-1 deferred | — |
| 1 | `auth-log-scan` | `cb81cf4` | `finding` · metadata (R-1) | `clear` | `finding` | `clear` | `clear` | A-1 closed · R-1 deferred | §5's cross-repo half |
| 2 | `apply-scout` | `0957ce1` | `finding` · metadata (R-1) · third-party data | `clear` | `finding` | `clear` | `finding` | E-2 closed · B-2 closed · D-2 deferred · R-1 deferred | four ADRs, the `llm` cassette half, the judgment set |
| 3 | `it-job-radar` | `e6e9859` | `finding` · metadata (R-1) · third-party data | `clear` | `finding` | `finding` | `finding` | E-3 closed · B-3 closed · D-3 closed · C-3 deferred · R-1 deferred | the notebook, `docs/plan/` and `docs/ideas/`, the Parquet row values |
| 4 | `pl-jobs-lora` | `56f09ab` | `finding` · metadata (R-1) | `finding` | `finding` | `finding` | `clear` | A-4 closed · B-4a closed · B-4b closed · B-4c closed · B-4d closed · B-4e closed · C-4 closed · R-1 deferred | the notebook end to end, two ADRs as arguments, the report's rows |
| 5 | `doc-extract` | `b4efae7` | `finding` · metadata (R-1) · third-party data | `finding` | `finding` | `finding` | `clear` | A-5 closed · E-5a closed · E-5b closed · E-5c closed · B-5d closed · B-5e closed · C-5 closed · R-1 deferred | the 79 result reports end to end, the attack payload text, `findings.md` as an argument, the merged PR bodies |
| 6 | `ab-lab` | `9900926` | `finding` · metadata (R-1) | `finding` | `clear` | `finding` | `finding` | A-6 open · C-6 deferred · D-6 closed · R-1 deferred | the eleven ADRs as arguments, the `slow` suite, the examples re-run, the failing marks rendered |

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

Scanned 2026-09-11 at index `cb81cf4`, gitlink `50e8b6e`, entry state clean. Four axes, because
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

Scanned 2026-09-11 at index `0957ce1`, gitlink `c7958eb`, entry state clean and `HEAD`
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
also the only headline the audit has read that leads with the project's **own weakest number**,
which is a deliberate and defensible choice: the page's argument is that the one link nothing
scored was the one every other metric depended on. The attack section is the strongest writing
the audit has read — it publishes **`exfiltrate` → succeeded every time** in both arms,
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
otherwise the best the audit has measured: MIT detected by GitHub from `LICENSE`, **eighteen topics**,
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

Scanned 2026-09-14 at index `e6e9859`, gitlink `1e65bfc`, entry state clean: index `HEAD`
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

### A-4 — `pl-jobs-lora`, session 4

Scanned 2026-09-17 at index `56f09ab`, gitlink `8fe2e02`, entry state clean: index `HEAD`
identical to `origin/main`, twelve pointers matching their own `origin/main`, nothing
uncommitted, no open portfolio pull request. **Five axes**, E being E0 and E2's third-party
half.

*This row was written on a local branch in the repository that has since become the archive,
and it reaches a reader by transplant.* The operator's standing instruction for the session was
that no work reaches a remote — no push, no pull request, no issue touched — with read-only
`git fetch` and `gh` permitted so the entry state and axis D could be answered at all. The scan
prompt's *"commit and push the index audit branch"* was therefore half-executed by design.
**Its second half is executed by the merge of the pull request carrying this line, and against a
different repository**: the three commits were cherry-picked onto `portfolio-index`, because by then
`current_projects` accepted no commits. *The sentence this replaces said the row was "published
by nothing" — which its own merge falsifies. `ST-1`, committed inside the one paragraph written
to stop a reader inferring a publication state that did not hold, and caught by reading the
paragraph before pushing it rather than by any instrument.*

**The measurements above and below are unchanged and stay frozen at the HEAD they name**, which
§1 requires of every figure in this document and §4 repeats for the axis cells. `56f09ab` is an
ancestor of this repository's `main`, and `8fe2e02` is the gitlink this row's own tree records,
so both resolve for a reader holding the published index — which they do because route A cloned
`main` without rewriting history. *That is a property of the route and not of this row*: under
`0011` §6's route B, `56f09ab` would have had to be re-derived. **The gitlink would not.** Route
B rewrites this repository's history and not the sibling's, so *"every SHA changes"* is simply
false about a submodule pointer. *This sentence said both would have to move, which is the
review of the transplant catching the transplant's own paragraph overreaching about the route
it was written to explain.*

*And the `Index SHA` cell means the archive's HEAD at scan time, not this repository's.* §4
defines that column as `git rev-parse HEAD` **of this repository**, which `portfolio-index` did
not satisfy on 2026-09-17: it stood at `edb2638`. The entry state quoted above has the same
shape, measured by a `tools/entry_state.py` whose `INDEX` still named `current_projects`. Both
cells are correct as measurements and neither meets the definition a reader of *this* repository
will apply to them, which is what a transplanted row owes saying rather than leaving a later
reader to derive the mismatch and file it.

**E0 — `finding` · metadata, and it is R-1's.** Three identities and no fourth:
`P0w3r223 <p0w3r2243@gmail.com>` 101 fields, GitHub's noreply 16, and
`Piotr Cząstkiewicz <p0w3r2243@gmail.com>` 9. **9 of 63** commits carry the real name,
reproducing R-1's table cell exactly by R-1's own method — counting commits, not fields.
`git rev-list --all --count` and `git rev-list main --count` both read 63, so no unmerged
history is hiding a fourth identity.

*The real name also stands in eight tracked files, and that is not R-1.* `LICENSE`:3's
copyright line, the `Author:` field of all six ADRs, and `docs/research/f6-data-availability.md`:5.
That is deliberate authorship on the owner's own CV portfolio — the same shape `apply-scout`
carries in thirteen files and `it-job-radar` in eight — and no earlier session raised it.
Written down so a repair acting on R-1 does not sweep content R-1 was never about.

**E2 — `clear` · third-party data, and the reason is structural: this repository publishes
none.** That sentence is the difference from A-2 and A-3 and it decides the repair, so it comes
before the evidence.

*The committed data artifacts are six files and every one is invented.* **Four** JSONL under
`data/fixtures/labeling_qa/` — `processed/train.jsonl` holding three records,
`processed/test.jsonl` two, plus `proposals.jsonl` and `human_gold.jsonl` — carry `offer_id`
`fx-001`…`fx-005` and `url` `https://example.test/o/fx-00N`; `data/fixtures/offer_sample.html` is a synthetic
`__NEXT_DATA__` page whose employer is `Acme Sp. z o.o.` and whose id is `fixture-001`, and its
own first comment says *"Not real data"*; `data/normalization/tech_aliases.yaml` is a
vocabulary. No real posting prose, no employer, no person, in any of them. That directory's own
`README.md` states the exemption and `ADR-0005` carries the reasoning.

*The two committed result artifacts are aggregates and were read rather than assumed.*
`results/eval/report.json` holds `metadata`, four `variants`, `bootstrap` and `ceilings` — counts,
F1 means, confidence intervals and token caps. **No `offer_id`, no `url`, no `prose` key anywhere
in the structure**, and `results/eval/report.md` is its rendering.

*The derived dataset never reaches git, and where it does go the code makes it private.*
`.gitignore` excludes `data/raw/`, `data/processed/`, `data/dataset_slice.json`,
`results/eval/predictions/` and the three labeling-QA JSONL that echo prose. **Three of those
five groups name the ADR that decided them** — `:15` ADR-0002, `:37` ADR-0005, `:43` ADR-0003 —
and the S2 block at `:32`, which carries `data/dataset_slice.json` and `data/processed/`, names
none. `dataset/hf_dataset.py`:66 calls
`api.create_repo(repo_id, repo_type="dataset", private=True, exist_ok=True)` — so the freeze, if
and when it runs, is private by construction rather than by remembering.

*The closest thing to third-party content in the tree was read.*
`docs/research/f6-data-availability.md`:26 names one live offer by a generic title and city —
*Analityk systemowo-biznesowy*, Warszawa — and quotes **no prose**, only per-section character
counts. No employer, nothing identifiable to a person.

**What this is not, stated so a repair does not copy A-3's E-3 remedy into a repository that
does not need it.** `LICENSE` is MIT with no carve-out and there is no `NOTICE` — which in
`it-job-radar` was exactly the finding. Here that is correct, because the MIT grant covers no
third-party data: none is committed. The attribution sentence — *"Attribution: theprotocol.it,
reused via `it-job-radar`"* — stands in `README.md`:376 and `docs/index.html`:239 and **no test
holds either**, but it is a courtesy statement about data this repository does not distribute,
not a term withholding a right the licence grants. A `NOTICE` here would carve nothing out of
nothing.

*The cheapest observation that would falsify this `clear`.* `git grep -nI 'offer_id' -- data/
results/` returning an id outside `fx-`/`fixture-`, or `results/eval/report.md` turning out to
hold a per-record table rather than the four-variant aggregate it is. Both are one command and
neither was left to inference.

**A — `finding`, and it is one narrow defect against an otherwise strong module.** The
numbers first, from the instrument and not from reading: **233 tests pass** — in 2.64 s on this
machine, and a wall-clock second is the one figure in this row no reader can reproduce — and
`ruff check .` reports *All checks passed!*, both under the repository's own
`.venv/Scripts/python.exe`, which carries the editable install CI produces with
`pip install -e ".[dev]"`. §6's 2026-09-14 correction did not bite here — the install path
existed, so no `PYTHONPATH` was needed, and this row says which was used because that row
says to.

Error handling is the strong half: across **30 modules** in `src/` there are
**zero bare `except`, zero `except Exception`, zero `except BaseException` and zero `Any`
annotations**, and all six `except` handlers name their type. An AST walk finds
**four functions over `good-practices.md`'s fifty lines** — `train/qlora.py`:122
`run_training` 94, `eval/bootstrap.py`:141 `bootstrap_variants` 72,
`inference/predict_gguf.py`:52 `run_gguf_predictions` 56 and `eval/bootstrap.py`:265
`render_markdown` 51 — and the largest module, `dataset/labeling_qa.py`, is 391 lines.
Nothing approaches the 800 ceiling.

**The finding is `dataset/collect.py`:195, and it is the same shape A-3 cleared in the sibling
for precisely the opposite reason.** Inside `_fetch_examples`:

```python
except requests.RequestException:
    continue
```

Nothing is recorded. `it-job-radar`'s `collect/theprotocol.py`:193 is the same handler over
the same platform and A-3 cleared it explicitly *because* `state` is initialised to
`FETCH_FAILED` before the `try` and a `finally` writes the outcome into the frame, leaving the
URL eligible for retry. Here the URL is dropped and the only signal a run emits is
`print(f"[collect] {len(urls)} urls -> {len(out)} usable")` at `:207` and `:223` — one gap
folding **three** different causes: a request that failed, a page `parse_offer_page` returned
`None` for, and an offer dropped by `data.min_prose_chars`. `good-practices.md` §3 names this
by its name, and §3's own remedy applies without redesign: the loop is right to drop a bad URL,
so the fix is a counter, not a raise.

*What makes it worth a row rather than a note is what the README does with that gap* — see
**B**, where the whole `800 → 710` difference is attributed to deduplication, and this is the
handler that can also produce it.

**And that path is exercised by nothing, measured rather than assumed.** A stdlib call-tracer
over the suite — `sys.settrace`, no dependency installed — reports **51 of 201 functions in
`src/` are never called**, and `collect.py`'s entire network half is six of them: `_session`,
`fetch_sitemap_urls`, `_spread_sample`, `_fetch_examples`, `collect_dev_slice` and
`collect_dataset`. `tests/test_collect.py` holds five tests and every one of them enters
through `parse_offer_page` over the synthetic fixture; `git grep` for `RequestException`,
`raise_for_status` or `status_code` across `tests/` returns **nothing**.

*Most of the 51 are defensible and this row says so before naming the four that are not.* They
are the I/O boundary the architecture isolates on purpose — model loading, HF Hub push/pull,
MLflow, the CLI `main`s, the paid API client. **Four are pure functions with branches:**
`collect.py`:175 `_spread_sample`, whose `n >= len(urls)` short-circuit and
`step = max(1, len(urls) // n)` guard are exactly the arithmetic a sampler gets wrong;
`eval/report.py`:80 `best_recall`, whose `None`-filter decides what a ceiling is compared
against; and the two `as_dict` serialisers at `eval/bootstrap.py`:71 and `eval/ceiling.py`:59.
A pure function is the cheapest thing in this repository to test and these four are the ones
the split does not excuse.

**The artifact the page stands on is verified by nothing in the suite — and it currently
holds.** `tests/test_docs_page.py` is the **only** test that opens the committed
`results/eval/report.{md,json}`, and it opens them as the *source of truth* the page is checked
against, never as an artifact to validate; `tests/test_eval_report.py`'s 283 lines build
synthetic reports in `tmp_path`, and `write_report` is in the never-called list above. So the
chain is page → `report.md` → nothing. **This session closed the loop by hand**: reconstructing
`ComparisonReport` from the committed `report.json` and calling `render_markdown()` reproduces
the committed `report.md` **byte for byte**, and `as_dict()` round-trips the JSON exactly. The
finding is therefore not a divergence but a carrier — one test, and the property is held.
*Its limit, stated:* this proves the two committed files agree with each other, not that either
reflects the gitignored `results/eval/predictions/` they were computed from. Nothing committed
can prove that, which is the same boundary `ADR-0004` draws in the index.

**The `0010` §5 loop shape was looked for and is not here — recorded because a negative from a
sweep is worth more than an unasked question, and measured because this row's own first draft
asserted the direction from reading.** Both module constants the page guard iterates fail
**closed**, run as §3.6 asks with a collected-green baseline and the mutation applied in
memory: unmutated, both tests pass; with `ARTIFACTS` emptied the provenance test goes **red**
(*"the page prints ['0', '0.01', …]"* — every figure becomes unsourced), and with
`TILE_SOURCES` emptied the tile test goes **red** on
`assert len(tiles) == len(TILE_SOURCES)` against the page's own four tiles. `test_agreement.py`:116's
`for b_name in BUCKETS` iterates a vocabulary the module defines and the assertions around it
name buckets literally. This is the first of the four scanned repositories where that shape is
absent rather than mitigated.

**One citation inside a guard resolves to nothing, and it is `CLAUDE.md`'s own warning in a
sibling's tree.** `tests/test_docs_page.py` cites `ADR-0012` twice — at `:39` for the rule that
admits a committed non-generated source, and at `:192` as the authority for the whole
provenance test. **This repository's ADRs run 0001–0006**, and the index's run
0001–0009; `ADR-0012` exists only as `apply-scout/docs/decisions/0012_the_page_quotes_the_artifacts.md`.
The same file qualifies its other cross-repository citation — *"`ADR-0004` (in the private
index)"* at `:3` — so the convention is known and applied once out of twice. And `ADR-0004` is the
sharp case: **this repository holds its own `docs/decisions/0004-training-infra.md`**, so a
reader who drops the qualifier lands on a training-infra document. **The index already has
the instrument and it is pointed the wrong way**: `python -m tools.citations` classifies
`docs/audit/0007`:528's own `ADR-0012 §2` as `foreign` — *names a document this index does not
carry*. It reads the index's 69 tracked files and no submodule's, so the same citation two
directories down is invisible to it.

*And the sentence above falsified itself as it was written, three times, which is a better
finding than the one it was trying to make.* Its first draft said `foreign` held *"exactly one
such row"* — and writing that sentence quoted the reference, which made it two; correcting the
figure in the errata below quoted it again, which made it three. **The instrument cannot tell a
citation from a quotation of one**, so a census of foreign references is not stable under being
described, and every figure typed into this paragraph is a figure this paragraph invalidates.

**No count is given here on purpose.** `python -m tools.citations` prints the current one, and
the index reaches the same conclusion for the same reason in `tools/pagespec/__main__.py`'s
`GATE` — *"the surviving count is printed above rather than typed here"*, where *above* is the
run's own `gate policy` block. `CLAUDE.md` says it twice in its own words and not in these.
*This quotation was attributed to `CLAUDE.md` until the review of the transplant: the sentence
is in neither its `56f09ab` nor its current text, and "printed above" would mean nothing in a
file that prints nothing. A quotation resolving to the wrong file is the class named on
2026-09-17 — `tools/citations.py` answers whether a section exists, never whether it holds
what the citing line says it holds — and this one names no section at all, so no instrument
here could have been the one to ask.* Nothing gates either way: only
`unresolved` does, and it is 0. **Found by the `code-reviewer` pass, not by this session's
battery** — the third time that pass has caught a class the battery structurally cannot, after
the two `0010` §5 already records, and the first time the class was *self-reference* rather than
staleness.

**The two integers that reach that divisor are the two `config.py` does not validate.**
`_validate_train`, `_validate_eval` and `_validate_labeling_qa` are called at load and between
them raise on twenty-odd out-of-range values — `lora_r` positive, `dev_fraction` within (0, 1),
`latency_percentiles` within [0, 100], `human_sample_size` positive. **`data` and `probe` get
no validator at all**, beyond `:145`'s *"the base-model probe needs at least two candidates"*.
So `data.sitemap_offers_sample` and `probe.dev_slice_size` — the two knobs that become
`_spread_sample`'s `n` — are the unchecked ones, and a `0` in `configs/config.yaml` surfaces as
`ZeroDivisionError: integer division or modulo by zero` from inside the collector rather than as
a configuration error at load. *Verified, not reasoned:* `_spread_sample(["a","b","c"], 0)`
raises it. `good-practices.md` §2 is the rule — validate at the boundary, and make the interior
trust what it is given — and this file follows it for three sections of five.

*The cheapest observation that would falsify the rest of this axis.* Run the never-called census
against a **mutated** suite — delete `tests/test_docs_page.py` and confirm the count moves — since
a tracer that silently attached to nothing would report the same 51 for the wrong reason. And for
the byte-identity above: regenerate nothing, but change one digit in the committed `report.json`
and confirm the round-trip stops matching; a comparison that passes on any input proves as little
as a guard that cannot fail.

**B — `finding`.** Five, ordered by what a reader loses. The axis was bound by artifact rather
than by file, as the prompt says: every figure, flag and platform name the docs claim, against
whatever in the repository still produces it.

**B-4a. The README reproduces the evaluation table with three cells rounded away from what
`results/eval/report.md` prints — and the commit that corrected four other cells of that same
table is the one titled *"the README is a surface too"*.**

| README `:246`–`:247` | `results/eval/report.md` | |
|---|---|---|
| `102.6` | `102.58` | a figure no artifact prints |
| `2.5` | `2.47` | a figure no artifact prints |
| `4.7` | `4.68` | a figure no artifact prints |
| `67.9` | `67.90` | **legal** — `0007` §5.0 calls a trailing zero typography |

`305f4e2` (2026-09-06, #15) went through that table by hand and fixed **four cells in two
rows** — `21.4`→`21.43`, `103.0`→`103.02`, `2.3`→`2.25`, `4.1`→`4.13` — and left the other two
rows exactly as they were. **No guard was added in that commit or since**: a `git grep` for
`README` across `tests/` is empty, so the README is read by nothing, while `docs/index.html`
has 327 lines of `tests/test_docs_page.py` over it. This is `CLAUDE.md`'s own standing rule
arriving from outside — a hand pass over a table is a hand count, and a hand count in this
portfolio has produced 15, 18 and 19 against a true 20.

*Measured, and the measurement's own blind spot named.* The README's figures were swept
against **all 81 committed non-README files** — `git ls-files` returns 82, which is §2.1's own
inventory figure for this repository, still current, as is its `63` commits — using the
repository's own `_canonical` and `_NUMBER` from `tests/test_docs_page.py`, over a README body
with fenced code blocks and markdown link targets removed: **96 figures, 3 that nothing else
prints** — `76`, `4.7`, `102.6`. *The first run of this sweep quoted **76 files**, which was its
own filter's selection and not the corpus*: it dropped `.gitignore`, `.mcp.json`, `CLAUDE.md`,
`LICENSE` and the notebook. Re-run over all 81 the three unsourced figures are identical, so the
verdict never depended on it — but a sweep reported as *all* when it was a subset is the defect
this row raises against other people's figures.
**`2.5` is not among them and is wrong all the same**, because `configs/config.yaml`:10 and
`ADR-0001`:42–43 spell the model key `qwen2.5-1.5b` in lower case, which donates a bare `2.5`
to the source side. The page guard's exemption for that shape is case-sensitive **and applied
only to the page side**, never to the artifacts. It was found by reading the two tables against
each other, which is the observation: the sweep caught two of three, and no sweep of this
design catches the third.

**B-4b. The build census is carried by a file `.gitignore` excludes, and two of its figures pass
a naive sweep only by accident.** README:113–115 states *"800 offers fetched → 710 records (90
reposts deduplicated by id and prose hash), split 568 train / 142 test … title & work-mode
100 %, seniority 99 %, expected-tech 76 %, salary 31 %"*. The artifact that produces those
counts is `data/processed/manifest.json`, which `.gitignore`:34 keeps out of the tree. The
sentence carries **nine** figures — `800, 710, 90, 568, 142, 100, 99, 76, 31` — and of those
only **four** are checkable as the thing the sentence claims: `710` in `ADR-0002`:71, `568` in
`configs/config.yaml`:109 and `ADR-0006`, `142` in `results/eval/report.json`, and `31 %` in
`ADR-0006`:94. **`76 %` is printed by nothing at all.** Of the remaining four, `100` resolves
honestly enough elsewhere, and the other three survive a sweep on a technicality, in two
different ways. `90` and `99` are "printed" only because
`ADR-0006`:114 and `configs/config.yaml`:110 write `p90` and `p99` about token-length
percentiles — a tokeniser reads the digits and cannot read the `p`. And `800` is worse, because
it resolves to something that *looks* like its subject and is not: `ADR-0002`:12 asks for
*"400–800 examples"* and `configs/config.yaml`:119 sets `sitemap_offers_sample: 800`, so a
reader checking *"800 offers fetched"* finds the **target** twice and the fetched count never.
So the reposts count, the seniority coverage and the fetch itself are unverifiable and *look*
verifiable, which is worse than either.

*And this is where **A**'s finding lands.* The whole `800 → 710` gap is attributed to
deduplication. `collect.py`:195 drops a `RequestException` into that same gap without recording
it, so the sentence's arithmetic is not merely uncheckable — its *explanation* is one the code
can silently falsify.

**B-4c. The freeze on the HF Hub is stated as done on the published page and as deferred in the
README, and the page's copy is invisible to a single-line grep.** `docs/index.html`:237–238 —
*"the processed dataset is frozen | on the Hugging Face Hub"* — against README:109,
*"freezing them on HF Hub (`--push`, needs `HF_TOKEN`) is **deferred** until the dataset repo is
provisioned"*, with README:374 taking the page's side **265 lines below** README:109 — the
same file contradicting itself, not two documents disagreeing. The
repository's code agrees with README:109: `configs/config.yaml`:122 reads *"push deferred (needs
HF token)"* and `dataset/hf_dataset.py`'s first docstring says the push is *"intentionally not
run during S2"*. Whichever way the owner resolves it, **one of two published sentences is false
today**, and a recruiter reads the page.

*Recorded as a method note as much as a finding:* a grep for the page's sentence returns
nothing, because the claim wraps across a line break between `frozen` and `on`. That is the
second repository in which a finding's own text was the thing a single-line grep could not
see — A-3's D row was the first, and the guard written there folds each line with the next for
exactly this.

**B-4d. `ADR-0004`'s amendment retired Colab, named the two classes of site it had fixed, and
fifteen lines outside those two classes still say Colab.** The amendment is honest and its claim
is **true as written**: *"The docstrings and README that said 'Colab' now say hosted GPU"* — a
grep for `Colab` across `src/` returns nothing, and the README's two remaining hits are both
retrospective. What no sentence covered is everything else. **Nine lines in five files a contributor acts
on**: `pyproject.toml`:17 (the dependency-split rule, *"installed ONLY on Colab"*, which
`CLAUDE.md` restates as a hard rule) and `:60`; `.github/workflows/ci.yml`:16; `.gitignore`:9;
`configs/config.yaml`:87 (*"Colab-only trainer"*) and `:98` (*"free-Colab T4/P100"*);
`requirements-train.txt`:1, `:4` and `:5`. *This read **eight** through two rounds of errata,
against an enumeration that has always listed nine and against the fifteen the same errata
corrected `fourteen` into. The instrument is `git grep -ci colab` per file — 2/1/1/2/3 at
`8fe2e02`, which is the nine — and it was never run for this figure because the figure was
never doubted.* **And six lines across two sibling ADRs**:
`ADR-0003`:35, and `ADR-0006`:17, `:18`, `:36`, `:63` and `:104` — the last a step heading,
`## Colab Step 0`, that a reader on Kaggle would follow. **The unit is the line and not the
sentence**, because `ADR-0006`:17–:18 is one sentence carrying two of them; `git grep -c` counts
lines, and a count given in sentences is a count no instrument reproduces.

*This count was wrong twice before it was right, and the second time is the instructive one.*
The first draft hand-counted twelve. The correction measured fourteen with `git grep -c 'Colab'`
— **case-sensitively**, which silently dropped `requirements-train.txt`:**1**,
`# COLAB-ONLY training dependencies — DO NOT \`pip install\` these locally.`, the loudest line in
the file and the first thing a reader of it meets. A vocabulary sweep that is case-sensitive is
a sweep that trusts the writer to have been consistent, which is the assumption the finding
itself refutes.

*And the third time is instructive too, because the command named here did not produce the
figure beside it.* `git grep -ci colab` at `8fe2e02` reads **34 lines in ten files**. The
fifteen is what survives three exclusions the paragraph had not written down: `ADR-0004`
itself, which is the decision under discussion and carries 14 of the 34; `CLAUDE.md`'s 3, which
state the *rule* — hosted GPU is Kaggle, not Colab — and are therefore not residue; and the
README's 2 retrospective hits. 34 − 19 = 15, and 15 = the nine manuals plus the six ADR lines
enumerated above, so the figure was right and its stated instrument was not. *This is the §5
shape below — a figure from an instrument whose granularity or scope is not the claim's — and
its tell here is the one that bullet names: the exclusions were the interesting part and they
lived only in the reader's head.* The commands that do reproduce are per file: 2/1/1/2/3 for
the nine, and `git grep -ci colab -- docs/decisions/0003-*.md docs/decisions/0006-*.md` for
the six.

This is `0010` §5's newest shape — *an amended ADR is a fan-out* — on its **second** repository,
and it sharpens the entry: in `it-job-radar` the fan-out reached GitHub metadata a commit cannot
carry, and here it reaches the packaging, the CI and the ignore file, which a commit carries
perfectly well and which no sweep was run over. The amendment names *docstrings and README*; the
defect is that naming the classes you fixed reads, to the next reader, as naming all the classes
there are.

**B-4e. Two smaller claims the tree does not hold.** `.gitignore`:38 says *"only the numbers-only
`report.{json,md}` under `results/labeling_qa/` is versioned"* — **nothing under
`results/labeling_qa/` is tracked**, and `git log --all` over that path is empty, while the same
sentence is true of `results/eval/`. And the census in `tests/test_docs_page.py`:~205 —
*"262 figures admitted, 39 of them bare one- or two-digit integers"* — **was exactly right when
it was written** and went stale **one commit later**: recomputed at `879b5df` with `879b5df`'s
own tokeniser it is 262. **It took two commits and two unrelated causes to reach today's
251, and the row's first draft credited both to one.** `305f4e2` added `_canonical`, folding ten
trailing-zero duplicates → **252**; `36524c4`, the `Author:` migration, replaced the handle
`P0w3r223` in the two ADRs on the artifact list and took the figure **`223`** with it → **251**.
That last one is the detail worth keeping: the figure the artifact set lost is the one the same
test file's `_META_CONTENT` comment names by hand — *"reading them as claims makes the account
handle's `223` a figure the page has to source"*. The `39` survives both, because a bare integer
has no trailing zero to fold. **And the same comment's other figure is stale too, unremarked
until the review**: it says *"56 of the **59** figures this page prints"*, and the page prints
**58** today. *Recorded as a correction to the record's own practice
rather than as sloppiness*: the figure came from an instrument, and the commit that changed what
the instrument counts did not re-run it — which is `0008`'s rule about a measurement frozen into
prose, four lines from the code that produces it.

**Flags: the flag bullet's fourth repository, and the sweep's second new occurrence.** The
per-(module, flag) sweep ported from `apply-scout` reports **8 flags argparse defines that no
documented command line shows**, and **0 the docs show that argparse does not define**. Two
matter. `--fresh` (*"recompute every record instead of resuming from the predictions file"*) is
defined **twice** — `inference/predict_gguf.py`:141 and `inference/predict_hf.py`:207 — and
README:220 shows it under `predict_gguf` only; `predict_hf` is the **hosted-GPU** entrypoint,
where re-running is the expensive one. And `probe.py`:266's `--candidates` appears in **neither**
`README.md` nor `CLAUDE.md` in any form. The remaining six are `--limit` on five further modules
and `dataset/run.py`'s `--push`, both of which the README documents in prose for one module and
in no command line for the others.

*The cheapest observation that would falsify this axis.* For **B-4a**: regenerate
`results/eval/report.md` and confirm the three cells still differ — if a re-run moves the report
rather than the README being stale, the finding inverts and the README is the accurate one. For
**B-4d**: read `notebooks/train_qlora.ipynb` end to end rather than by grep; it is the one file
that would settle whether any *executable* step still assumes Colab, and this session read only
its imports and its secrets cell.

**C — `finding`, and the checker is not the one that found it.** §3.3's command first, as the
prompt requires: `python -m tools.pagespec --only pl-jobs-lora` reads

> `pl-jobs-lora   clear, 3 undecided`

and exits 0. The three are `4 h1` (a headline the checker cannot judge), `contrast marks`
(*no site; 75 outside D5's obligation*) and `contrast ground` (*0 sites without a resolved
ground*). Every gated clause passes, `contrast text` measures **34 of 34 sites, worst 5.17:1
against a 4.5:1 threshold**, and clause 1 declares eleven tokens with both schemes present.
**§2.2's baseline says *"4 or 5 undecided each"* and this run says 3** — §6's warning row, working
exactly as written: the marks census moved under `ADR-0008` §10 and the row quotes the run the
session made.

**The figure an auditor would flag first is the one thing here that is completely correct, and
it is recorded because the check cost something.** The h1 claims **94 %** — a ratio, and `0007`
§5.0 forbids a re-derivation as firmly as it forbids a rounding. It is neither:
`results/eval/report.md`:36 prints the sentence itself — *"`tech_expected`: 0.27 of a ceiling of
0.28 — **94 % of what the input makes recoverable**"* — so the page quotes the artifact's own
words, and `0.2657 / 0.2823 = 0.9412` reproduces it from `report.json` besides. The page
computes nothing.

**The finding is what that headline is about.** *"The best available model"* is
`claude-haiku-4-5`, few-shot — a purchased API baseline. The project's own row, `QLoRA (ours)`,
is still `–` across every column, which the status card says plainly three lines below. So the
page's largest claim, its `<title>`, and its `og:title` are a figure about **someone else's
model**, and `og:title` carries it without even the `— pl-jobs-lora` suffix the `<title>` has:
a link pasted into Slack or LinkedIn renders as a bare boast with no subject and no project
name. That is the one surface fragment a recruiter meets before deciding whether to click.

*Three smaller things in the same sixty seconds.* The h1 **names no field**: the 94 % is
`tech_expected` recall against a model-free ceiling, and read alone it is an overall-accuracy
claim, where overall field F1 is 0.51. The sub's **first** sentence — *"A field scored 0.01 for
every model, the frontier baseline included — which is usually not a measurement of the
model."* — needs two readings: it withholds the field's name, offers `0.01` with no scale, and
turns on a double negative. And **what the project is** arrives in the sub's third sentence,
about seventy words in; the first screen runs 120 words before the status card.

*Proposed wording, shorter and not more generic — every figure in it is one an artifact already
prints, so the page guard still passes.*

| | |
|---|---|
| h1 today | *The best available model recovers 94% of what the input makes recoverable* |
| proposed | *A frontier API reaches 94 % of a model-free 0.28 ceiling* |

The replacement is **11 words against 12, and 56 characters against 73** — measured, because
the first draft of this row claimed *two words shorter* for a replacement that was five words
longer, which is the defect B-4a is about, committed inside the paragraph proposing the repair.
It names **whose** 94 % it is, and puts `0.28` — the model-free ceiling, this repository's
genuinely original measurement, currently in a tile below the fold — beside it. Both figures are
in the guard's admitted set, so the page test still passes. Then move the sub's third sentence (*"A QLoRA
fine-tune of a small Polish LLM that turns job-posting prose into structured JSON…"*) to first,
where the `description` meta already has it, and give `og:title` the same `— pl-jobs-lora`
suffix `<title>` carries.

**What is right here, said because a row of findings misrepresents this page.** The status card
is the best the audit has seen at its job — *"in progress — baselines measured, fine-tune
pending… its two rows are shown empty rather than estimated"*. The two `note` paragraphs refuse
two easy overclaims by name: the local rows are priced `–` and **not** `$0` because no marginal
cost was recorded, and their latency is CPU time and *"not comparable to the API's"*. And there
is a whole section headed *"Correction: the salary numbers published before 2026-08-18 were
wrong"*, with the withdrawn figures struck rather than deleted — the behaviour `0008`'s errata
sections exist to encourage, on a public page, unprompted.

*The cheapest observation that would falsify this axis.* Open the page at 360 px and check
whether `.table-wrap` actually scrolls the eight-column table — clause 3 reports the scroller is
**declared**, which is not the same as reading it in a viewport, and this session judged the
markup and never rendered it. That is not this session's invention: `python -m tools.spec` lists
`c3.s2` — *"The wrapper must actually have somewhere to scroll when the table needs it"* — among
the sentences **carried by nothing**, with `ADR-0004` §4 recording the decision to defer it. So
the falsifier for this row and the portfolio's open geometry question are one measurement.

**D — `clear`, and it is the cleanest of the four scanned so far.** `gh issue list --state open`
returns **nothing**, and `--state all --limit 30` also returns nothing — this repository has
**never had an issue**, so A-3's own falsifier for a clean D (a *closed* issue describing code
that has since moved) has no subject here. `gh api .../branches` lists exactly `main`: no stale
branch. The last CI run, `34334073914` on 2026-09-09, is `success`, and so is the
`pages-build-deployment` beside it. `licenseInfo` reads `mit`, matching `LICENSE` and
`pyproject.toml`'s `license = "MIT"`. `homepageUrl` is
`https://p0w3r223.github.io/pl-jobs-lora/`, which is the surface `sources.SURFACES` reads.

**A finding was written and then withdrawn, and the withdrawal is the useful half.** The
repository description read, through `gh repo view --json description` piped into this session's
console, *"an honest accuracy `Ă—` cost `Ă—` latency comparison"* — which is exactly what a UTF-8
`×` looks like after a CP1250 round trip, on the repository's front door, twice. Fetched as bytes
instead — `gh api repos/... --jq .description` written to a file and decoded explicitly — the
description holds **one non-ASCII codepoint, `U+00D7 MULTIPLICATION SIGN`, twice, and both are
correct**.
The mojibake was this session's pipeline and never GitHub's.

*This is the second instance in two sessions of one class*, and §6 gains its entry: session 3
nearly raised 18 `ModuleNotFoundError` collection errors as a repository finding when they were
an environment verdict. **An instrument's own encoding is part of the instrument.** A `gh`
reading that shows mojibake in this environment has to be re-taken as bytes before it is a
finding, and the cost of not doing so would have been a correction filed against a repository
that is correct.

*Two things checked and deliberately not raised, so a repair does not raise them from the
row.* **The eight GitHub topics and `pyproject.toml`'s five `keywords` diverge in both
directions** — `llm`, `nlp`, `polish`, `python`, `structured-outputs` are topics only;
`polish-nlp` and `structured-extraction` are keywords only. `apply-scout`'s `CLAUDE.md` states
the rule that would make this a defect — *"`pyproject.toml`'s `keywords` lead; the GitHub topics
copy them"* — and **this repository's `CLAUDE.md` does not carry it**, exactly as A-3 found for
`it-job-radar`. Measured across all five scanned, **only `apply-scout` states it** — `auth-log-scan` lacks it too and was never checked for it in A-1 — so it is **four of five**, which promotes
it from a per-repository observation to the single cross-repo sweep A-3 asked for. And the
description's *"QLoRA fine-tune turning Polish IT job-posting prose into structured JSON"* is in
the present tense for a fine-tune that has not run — but unlike A-3's D-3, which advertised a
technology an ADR had **dropped**, this advertises the project's stated goal under the project's
own name, and the page's status card says *"fine-tune pending"* in its heading. Naming a goal is
not the same defect as advertising a retirement.

*The observation that would have falsified this `clear` was run rather than written down.*
`gh run list` cannot distinguish *CI passes* from *CI passes on the one workflow still enabled*,
because a **disabled** workflow never appears in a run listing.
`gh api repos/P0w3r223/pl-jobs-lora/actions/workflows` answers the question directly: two
workflows, `.github/workflows/ci.yml` and `dynamic/pages/pages-build-deployment`, **both
`active`**, and the first is the only workflow file the tree holds. What is left un-falsified is
narrower: this session never confirmed that the homepage actually answers 200 — §3.3 puts this
repository outside `--fetch`, so the surface was judged from the committed file.

**A-4 errata, 2026-09-17 — three rounds, and the rounds found different classes.** Recorded
rather than quietly fixed, because `CLAUDE.md` says to and because *what* was wrong is the
point: the row spent its B axis on a hand pass over a table and a figure frozen into prose, and
then hand-counted three times. **Round one was this session's own battery** — seven corrections,
six of them hand counts, every one findable by re-reading. **Round two was the `code-reviewer`
pass** — ten more, and not one of them was re-readable: each needed a command re-run against a
state the row had already moved past. **Round three was the `code-reviewer` pass over the
transplant**, recorded at the end of this section. *That division is the row's most portable
result.* `0010` §5 records that this pass has twice caught a class the battery structurally
cannot; rounds two and three are the third and fourth, and now with a stated mechanism — **a
battery checks whether a figure is right, and a second reader checks whether it is still right,
and about the thing it names.**

*No total is written here, and the header carried one until round three.* It read **eighteen**,
which was seven plus eleven, and the eleven counted a row whose own middle cell says
`unchanged` — *"both fail closed"* → *"measured"*, round one's fix confirmed independently,
which is a confirmation and not a correction. A hand count of a table, inside an erratum about
hand counts, in a document whose standing rule is that figures come from an instrument. The
derivation, for a reader who wants a number: count the rows below whose middle cell is not
`unchanged`. That keeps answering after round four; a typed total does not.

| what it said | what it says now | how it was wrong |
|---|---|---|
| *"the committed data artifacts are **seven** files… **five** JSONL"* | six files, **four** JSONL | a hand count. `git ls-files data/` returns nine paths, two of them `.gitkeep` and one that directory's `README.md`; *"three train, two test"* counts **records** and was read back as files |
| `f6-data-availability.md`:29 | `:26` | a line number read off a `sed` window's offset instead of `grep -n` |
| `.gitignore`:33 | `:34` | the same, twice: `:33` is `data/dataset_slice.json` |
| `.gitignore`:40 | `:38` | `:40` is `results/labeling_qa/review_queue.jsonl` |
| *"**twelve** sites… **four** sentences in two sibling ADRs"* | **fourteen lines**, six of them in the ADRs | a hand count in a unit the enumeration did not use. `git grep -c` counts lines; `ADR-0006`:17–:18 is one sentence over two of them, so *sentences* and *lines* disagree and the row mixed them |
| *"the replacement is **two words shorter**"* | 11 words against 12 | the proposal as first drafted was **five words longer** than the headline it replaced — an unmeasured comparative inside the paragraph proposing a repair for unmeasured figures |
| *"both fail **closed**"*, asserted from reading | the same verdict, now measured | §3.6's battery, applied in memory: green unmutated, red with each constant emptied. The claim was right; the method was not |


*Round two — found by the `code-reviewer` pass, against this row's first edition and round one's
corrections.* **No SHA is given for that edition**: the archive branch was rebased after the
review ran, so the commit the reviewer read is reachable from nothing there and was never in this
repository at all.

| what it said | what it says now | how it was wrong |
|---|---|---|
| *"one of exactly one such row in **1 975** references"* | no figure at all, and the reason given | **the sentence falsified itself as it was written, three times over**: quoting `ADR-0012 §2` made `tools.citations` count a second foreign reference, and correcting the figure in this very table made it a third. The instrument cannot tell a citation from a quotation of one, so the count is unstable under description and the row now refuses to carry it |
| *"the **next** commit added `_canonical`… and the sentence now reads 251"* | 262 → **252** (`305f4e2`) → **251** (`36524c4`) | two commits and two unrelated causes credited to one. The second is the `Author:` migration taking the figure `223` out of the artifact set — the very figure that test file's own comment names |
| *"**fourteen** lines still say Colab"* | **fifteen** | the correction was measured with `git grep -c 'Colab'`, case-sensitively, which drops `requirements-train.txt`:1's `COLAB-ONLY` — the loudest line in the file |
| *"swept against **all 76** committed non-README files"* | all **81**; 76 was the filter's selection | a subset reported as a corpus. Re-run over all 81 the three unsourced figures are identical, so no verdict moved |
| *"of the **eight** figures… the other **four**"*, naming three | **nine** figures, four checkable | the sentence carries `100` and `31` too; the split lost `31 %` between the count and the enumeration |
| *"thirty lines from the README's own"* | 265 lines below README:109 | a clause with no noun and a distance that was never measured |
| *"each with the ADR number beside it"* | three of the five groups do | an overreach: the S2 block at `.gitignore`:32 names none |
| *"one non-ASCII **character**"* | one codepoint, **twice** | the same paragraph says *"twice"* two sentences earlier |
| *"233 tests pass in 2.64 s"* | 233 tests pass, 2.64 s on this machine | a wall-clock second is the one figure in the row no reader can reproduce |
| *"56 of the 59 figures this page prints"*, unremarked | the page prints **58** | the guard comment's *second* stale figure, which round one did not notice while correcting its first |
| *"both fail closed"* → *"measured"* | unchanged | round one's own fix, confirmed independently |

*The generalisable half, and it is not flattering.* The scan prompt's standing rules already
say **figures come from an instrument, never a hand count**, and this row cites that sentence
in its own B-4a. Every one of the six was produced by reading output that was already on screen
rather than by asking a command the question — which is the cheaper failure mode than
carelessness and the harder one to notice, because the number *looks* derived. The fix that
would have caught all six is mechanical: a count that appears in a row has to be pasted from a
command in the same breath, and a line number has to come from `grep -n` and never from
arithmetic on a window. **Nothing in the five verdicts moved**, across both rounds, and that is the
one thing these tables are not evidence for: eighteen corrections to the prose left
`E2 clear`, `A finding`, `B finding`, `C finding` and `D clear` exactly where the measurements
put them. The findings were measured; the sentences around them were not.

**One thing the scan prompt says about this repository that is true and incomplete.** §3.3's
axis-A paragraph reads *"Ten repositories carry `.codegraph/`; `doc-extract` and `pl-jobs-lora`
do not."* Correct — and this repository carries a **different** index, `.code-review-graph/`,
declared in a tracked `.mcp.json` and present on disk, with `CLAUDE.md` naming both the MCP
server and the `uvx code-review-graph` fallback. A session reading the prompt's sentence as *no
index here* would leave a working instrument unused. Not a finding against the repository; a
note for whoever scans `doc-extract`, which may or may not be the same case.

**Not checked.** `notebooks/train_qlora.ipynb` was read for its imports, its secrets cell and its
output state (**zero outputs, every `execution_count` null**) and **not end to end** — which is
the one gap that could turn B-4d from a documentation finding into a code one. The six ADRs were
read where a citation, a figure or a platform name pointed into them; `ADR-0003` and `ADR-0006`
were not read as arguments. `results/eval/report.json` was read by structure and by the four
tile cells the page quotes, **never row by row**. The GGUF and HF inference paths were measured
by the call-tracer and never executed, and nothing that costs money or a GPU was run. E1 was not
re-swept: §2.3's portfolio pass stands, and the targeted sweep this session ran over tracked
files found only the word *token* in its LLM sense, secret **names** rather than values, and
`kaggle_secrets` used correctly. The live page was not fetched — §3.3 puts this repository
outside `--fetch`, so axis C is the committed file's verdict.

**Round three, 2026-09-17 — the `code-reviewer` pass over the transplant.** Its subject was not
the scan: it was whether a row measured in one repository still reads correctly to a reader
holding another. Two of the rows below are the transplant paragraph's own and the rest are the
scan's prose, and **not one is an axis verdict, a table cell or an E-, A-, B-, C- or D-axis
figure** — the measurements reproduced to the digit when re-run against `8fe2e02`.

*No total is typed here either, and the first draft of this paragraph typed one: it said
**eight** over a table of nine rows.* One paragraph after mandating the derivation that prevents
exactly that, in the round whose subject is figures that do not survive their own description.
The derivation is the same one: count the rows.

| what it said | what replaces it | why |
|---|---|---|
| §5: *"It went stale at the **next** commit: `305f4e2` added `_canonical`… and the sentence now reads 251"* | two commits, two unrelated causes: 262 → **252** (`305f4e2`) → **251** (`36524c4`) | §4's round-two table corrects this exact sentence, and the correction was never carried into §5 — `ST-3`, in the bullet arguing that a census goes stale four lines from its instrument. The arithmetic said so unaided: 262 − 10 is 252 |
| *"**Eight** lines in five files a contributor acts on"* | **nine** | the enumeration under it has always listed nine, and the `fifteen` the same errata corrected `fourteen` into is nine plus the six ADR lines. `git grep -ci colab` per file reads 2/1/1/2/3 at `8fe2e02`; it was never run for this figure, because the figure was never doubted |
| a quotation attributed to *"this repository's `CLAUDE.md`"* | `tools/pagespec/__main__.py`'s `GATE`, with *above* naming the run's own `gate policy` block | the sentence is in `CLAUDE.md` neither at `56f09ab` nor today, and *"printed above"* means nothing in a file that prints nothing. The class named on 2026-09-17 — the resolver answers whether a section exists, never whether it holds what the citing line says — and this citation names no section at all, so no instrument here could have asked |
| *"`git grep -ci colab` reads fifteen"* | the bare command reads **34 lines in ten files**; fifteen is what survives three exclusions, now written down | the named command did not produce the figure beside it, and a reader re-running it had no route to fifteen. 34 − 14 (`ADR-0004` itself) − 3 (`CLAUDE.md`'s rule lines) − 2 (the README's retrospective hits) = 15 |
| §5's flag bullet: *"three repositories, three sessions"* | no count in the lead, and the reason | the paragraph appended under it **in this same session** documents a fourth, `pl-jobs-lora`'s `--candidates`. Every session so far has added one, so a lead figure there is stale by the next reader and is the sentence everyone quoting the shape carries |
| this section's header: *"**eighteen** corrections, in two rounds"* | three rounds, no total, and the derivation beside it | seven plus eleven, where the eleven counts a row whose middle cell reads `unchanged`. A hand count of a table, in an erratum about hand counts |
| the transplant paragraph: *"every SHA changes and this paragraph would have had to re-derive **both**"* | only `56f09ab`; **the gitlink would not** | route B rewrites this repository's history and not the sibling's, so *"every SHA changes"* is false about a submodule pointer. A claim about `0011` §6 that §6 does not make |
| the transplant paragraph: nothing about what the `Index SHA` cell means after a transplant | says whose HEAD the cell and the entry state are, and that neither meets §4's definition for a reader of this repository | §4 defines the column as `git rev-parse HEAD` **of this repository**, which `portfolio-index` did not satisfy on 2026-09-17. Correct as measurements, mismatched against the definition a new reader applies |
| *"the **private** index's ADRs run 0001–0009"* | *"the index's"* | the fact survived the move and the label did not. Nine ADRs is still right; the index a reader holds is public |

**Two of the eight are in the paragraph written to stop exactly this**, which is the round's
most portable result and the argument for the pass rather than for more care. A transplant is a
generator of the `ST` family by construction: every sentence whose premise is *this repository*,
*the private index*, or an entry state changes truth value without changing a byte, and the
paragraph that says so is not exempt. What no instrument here can do is ask the question —
`tools/citations.py` resolves a `§N` to a heading and stops, and `tools/spec.py` pins normative
sentences by literal, so a premise that rots inside otherwise-correct prose is reachable by
reading and by nothing else.

*Three findings from the pass are deliberately not taken.* The errata block sits as prose inside
the row rather than as its own `###`, unlike A-2's, so it is the one erratum unreachable from a
heading list — **left as it is, and the first reason offered for that was wrong.** It was that a
moved block would invalidate line citations into the row; `git grep -nE '0010:[0-9]+'` returns
nothing anywhere in the tree, including inside this document, because `0010` is cited by section
and only `0008` is ever cited by line. *Written down because it is this round's own instance of
the class the round is about: a reason that reads as derived and was not.* The reason that
survives measurement is smaller — the errata block is followed by A-4's *not checked* closing,
which belongs to the row and not to the errata, so a heading here needs that paragraph moved
too. Worth doing when A-5 lands and the section moves anyway. The `tests/`
citation of a submodule's own `ADR-0012` is a fourth occurrence of §5's last bullet and is not
added there, because that bullet asks for a link checker whose design is `architect`'s and a
fourth tally does not change the ask. And *"the index's 69 tracked files"* is left at 69: the
freezing rule covers it, `python -m tools.citations` prints 71 today, and re-deriving a frozen
figure is the practice §4's header exists to refuse.

### A-5 — `doc-extract`, session 5

Scanned 2026-09-17 against the archive's `main` at **`b4efae7`**, gitlink `7ae9c84`, entry state
clean: `HEAD` identical to `origin/main`, twelve pointers matching, nothing uncommitted.
**Five axes**, E being E0 and E2's third-party half.

*Two notes about that SHA, because a later reader will check it.* **First**, the scan ran on an
unpushed branch in the repository that has since become the archive, under the operator's standing
instruction that no work reaches a remote, with read-only `git fetch` and `gh` permitted — so the
working commit it was taken at is reachable from nothing and **is deliberately not cited**, which
is this row's own axis-A finding applied to itself. `b4efae7` is the archive `main` its `tools/`
was byte-identical to; it is in this repository's history, and it is what a reader can check.
**Its other half is executed by the merge of the pull request carrying this line, and against a
different repository** — the work was ported onto `portfolio-index`, because by then the archive
accepted no commits. *Written this way on a teammate's warning rather than after the fact: A-4's
round three records the same sentence falsifying itself when its merge published a row that said
it was published by nothing. `ST-1`, caught once by reading and once by being told.*

**Second**, `#141` and `#142` landed between A-4 and this session and touched `.github/`,
`CLAUDE.md`, `README.md`, `SECURITY.md` and the new `0011` — and **neither `tools/` nor `tests/`
nor `0010`** — so the checker that produced axis C below is the one those merges left standing.

*And one finding was raised on the entry state and withdrawn there.* This submodule carries a
**local branch `fix/the-tile-counts-the-result`, four commits, on no remote** — `gh api
.../branches` lists only `main` — whose subjects say the published page's fourth KPI tile *"counted
milestones, and counted them wrong"*. That reads exactly like finished work that never landed. It
is not: `main`'s `docs/build_index.py`:1578 says *"The tile used to read `5 / 7` milestones"* in the
past tense, and the committed page renders **`3 / 6` · Attacks the arithmetic never sees**, which is
what the branch's **third** commit describes building — `fae44eb` at 12:10, third by the clock and
second only in `git log`'s newest-first display, and named here in the knowledge that it is a
branch SHA no clone of that repository resolves, which is the point of the paragraph. The work was squash-merged and the local branch
was never deleted — `CLAUDE.md`'s own rule, *"a branch commit is never reachable from `main` and
never will be"*, in the one form it does not warn about: not *is this pull request merged*, but *is
this local branch's work already in*. The branch is stale housekeeping, invisible to GitHub, and
**not** a finding.

**E0 — `finding` · metadata, and it is R-1's.** Three identities and no fourth:
`P0w3r223 <p0w3r2243@gmail.com>` 91 fields, GitHub's noreply 15, and
`Piotr Cząstkiewicz <p0w3r2243@gmail.com>` 8. **8 of 57** commits carry the real name, reproducing
R-1's table cell exactly by R-1's own method. Unlike A-4's repository, `git rev-list --all` (57)
and `git rev-list main` (53) **disagree**, and the four are the stale branch above — swept by
`--all`, so no fourth identity hides in them. The name also stands in four tracked files —
`LICENSE`, the two ADRs and `docs/findings.md` — which is the deliberate authorship A-4 recorded
for the portfolio and not R-1's subject.

**E2 — `finding` · third-party data. Two vendored artifacts, an exemplary provenance discipline,
and the discipline applied once out of twice, in two different ways.**

*What is right here has to come first, because it is the best the audit has seen and the finding
is only legible against it.* `schemas/PROVENANCE.md` records source URL, publisher, publication and
retrieval dates, byte size, SHA-256, the fixed schema attributes, **the complete import closure**
(FA(3) pulls three more files by absolute `crd.gov.pl` URL, all vendored, with `tests/conftest.py`
mapping the URLs onto local copies so the suite compiles with remote fetching disabled), a
*"why it is vendored rather than fetched"* section, and a runnable re-vendoring script.
`src/doc_extract/assets/fonts/PROVENANCE.md` does the same for DejaVu. And
`tests/test_vendored_artifacts.py` turns both tables into constraints — its own docstring says
why: *"nothing was checking them, so the pin was documentation rather than a constraint"*. It even
carries a guard against its own vacuity, `test_the_provenance_documents_pin_every_artifact_that_matters`,
for a regex that silently stopped matching. **A-3's E-3 finding — terms stated in three places and
held by none — has no purchase here.**

**E-5a. The one vendored file whose absence is a licence problem is the one file that guard
excludes, and it says so.** `EXPECTED` names six artifacts, the four XSDs and the two fonts, and
the comment above it reads: *"The vendored `LICENSE` carries a digest too, but it has no bearing on
a rendered byte or a parsed schema."* True — and its bearing is legal rather than functional. The
vendored licence at `:67` requires that the notice *"shall be included in all copies of one or more
of the Font Software typefaces"*, so that file travelling with the two `.ttf` is an **obligation**,
not a courtesy. *Measured rather than reasoned, without touching the tree*: `declared()` matches on
`\.(?:ttf|xsd)`, so `LICENSE` is not in its output at all, `EXPECTED - set(declared())` is empty,
and **deleting `src/doc_extract/assets/fonts/LICENSE` leaves both tests green** while the fonts and
their digests stay exactly as recorded. The repair is one entry, and the provenance already records
the digest to hold it to.

**E-5b. The provenance template has a `Licence` row and the schema document does not fill it.**
The font document's rows are `What · Release · Source · Retrieved · Licence · File`; the schema
document's are `What · Source · Publisher · Published · Retrieved · Size · SHA-256 ·
Fixed attributes · File`.
Same author, same repository, both retrieved 2026-08-18 — and 268 kB of Ministerstwo Finansów XSD
sits under a root `LICENSE` granting MIT over the tree, with `README.md`:674's whole licence section
reading *"MIT."* **Nothing anywhere states on what terms the national schema may be redistributed.**
*Stated as an absence and not as a violation, deliberately:* Polish copyright law excludes official
materials from protection, so the likely answer is that no terms are needed — which is a sentence
the provenance document could carry in one line, and the point of the row is that it carries a
`Licence` row for a font and none for a government standard.

**E-5c. The corpus publishes 221 structurally valid NIPs, and the module that makes them states a
requirement its construction cannot deliver.** `synth/pools.py`'s docstring: *"the identifiers are
constructed to satisfy their check digits rather than copied from a register, so no real taxpayer
appears in the corpus. That is a requirement, not a courtesy — the alternative would put real NIP
numbers in a public repository."* The sentence one line below shows the author knows the difference
between two kinds of guarantee: the IBANs use bank prefixes *"drawn from ranges no bank uses, so an
account number cannot be mistaken for a routable one"* — **structural**. The NIP has only
provenance: *not copied from a register*, which is not the same as *not in one*.

*The arithmetic, from the generator's own rules and not from an estimate.* `nip()` draws nine
digits (first non-zero, second and third not both zero) and computes the tenth, discarding a
weighted remainder of 10 — **810 000 001 constructible values**, computed by residue DP over
`_NIP_WEIGHTS` rather than enumerated. The committed `results/` hold **221** distinct ten-digit
strings that `schema.checksums.is_valid_nip` accepts, out of 270 candidates. The collision
probability then depends on one number this session did **not** measure, the size of the real
register, so it is given as a table over assumptions rather than as a figure:

| if the register holds | P(at least one published NIP is real) |
|---|---|
| 1 000 000 | 23.9 % |
| 3 000 000 | 56.0 % |
| 5 000 000 | 74.5 % |

**So the requirement is not met, and at a plausible register size it is more likely than not to be
unmet.** *What this is not:* a NIP is public business data in Poland — printed on every invoice and
carried by CEIDG and the KRS — so a collision attaches a real company's public tax number to an
invented name, address and amount, and identifies no person. The severity is `third-party data` and
the defect is the **claim**, in a repository whose whole subject is the difference between a figure
that is checked and a figure that is asserted. The open question the repair inherits, and this row
does not answer: whether the NIP numbering scheme has an unassigned prefix range that would give
the same structural guarantee the IBANs already have.

*The cheapest observation that would falsify this axis.* For **E-5c**: nothing here proves a
collision, only that one is likely — checking even one of the 221 against a public register would
settle it, and the audit deliberately did not, because querying a taxpayer register about numbers
this repository published is a worse act than the finding. For **E2 generally**: the committed
`results/` were read for identifiers and reports, **never** for the extracted free-text values —
`predictions.jsonl` carries party names and addresses, and those were taken as synthetic on
`pools.py`'s word rather than diffed against the corpus manifest.

**A — `finding`, and it is one line of dead code against the strongest codebase the audit has
measured.
The proportion is the point, so the numbers come first.** **817 tests pass and 17 skip in 97.7 s**,
`ruff check .` reports *All checks passed!*, both under the repository's own `.venv`.

*The 17 skips were read, because **this document's** §3.6, second observation, is that a skip is
a pass.* They
are one parametrised test, `tests/test_results_committed.py`:219, skipping each run directory that
is not an attacked corpus — **17 of the 24 committed runs**, leaving exactly the seven
`attack-*`/`attacked-scanned-*` directories the listing holds. The arithmetic closes and the reason
prints beside each one.

Error handling is **the best the audit has seen**: across **77 modules and 14 523 lines** in `src/`
there are **zero bare `except`, zero `except BaseException`, and exactly one `except Exception`** —
at `extract/anthropic_client.py`:71, the only module that touches the network, where five lines of
comment explain that the SDK's failures *"have no single base class that can be named without
importing the SDK at module scope"*, and it is **re-raised** as `LLMError(...) from error`. All
**six _bare_ `Any`** annotations are at that same boundary plus one pdfplumber colour value; `src/`
carries `Any` **57 times across 13 modules** as a whole word — the first edition said 64 across 16,
which is what `git grep -o 'Any'` returns when it matches inside longer words — and the rest are
mostly `dict[str, Any]` payload maps at JSON boundaries, with one `tuple[Any, ...]` at
`extract/pipeline.py`:197. *The first edition said "all six", which reads as a total.* And all
**70 `print` sites** are in the **five** `__main__.py` CLIs and `generate_vocab.py`, which is a CLI
with a `--check` mode — **zero in library code**, where `it-job-radar` had 25 in one file and
`pl-jobs-lora` two in a library module.

Size holds too: **nine functions over `good-practices.md`'s fifty lines**, the longest
`attack/report.py`:242 `_caveats` at 88; five files over 400 lines and **none over 800**, the
largest `synth/render.py` at 603.

**The finding: `eval/scorer.py`:145 `score` is dead public code, in the module the project's
headline rests on.** It is documented — *"`judge`, for a run in flight, taking the failure class
off the extraction itself"* — and its body calls `judge`. **Nothing calls it.** The stdlib
call-tracer puts it among the never-called, and the static side agrees: every `from
doc_extract.eval.scorer import …` in the tree — nine of them, across `docs/build_index.py`,
`attack/outcome.py`, `aggregate.py`, `detector.py`, `selective.py` and four test modules — pulls
`judge`, `compare`, `Outcome`, `Result`, `DocumentScore`, `DETECTED` or `SUPPORTED`, and **not one
pulls `score`**. `eval/__main__.py`:325's `run.score(...)` is a different function in a different
module, which is exactly what makes this worth a row rather than a note: a reader scanning
`scorer.py` for the entry point finds a public function with the obvious name, and it is the one
nothing uses. `ruff` cannot see it — an unused module-level function is not an unused import.

**And the census that makes the verdict fair.** The tracer reports **20 of 627 functions in `src/`
never called — 3.2 %**, against `pl-jobs-lora`'s 51 of 201 at 25 %. Sixteen of the twenty are CLI
`main`/`_progress` glue and protocol members. Two are worth naming beside the finding:
`DocumentScore.template` at `scorer.py`:85, a property never read anywhere — while its neighbour
`tier` at `:81` is read in exactly two, `eval/detector.py`:135 and `:155` — and whose one-line body, `self.facet("template")`, is
duplicated verbatim at `aggregate.py`:176 and `dataset.py`:79. And **two of the five `summary_lines`
functions are reached by no test while three are**: `report.py`:228 and `attack/report.py`:337
through `eval_cli.main(["attack", …])` at `tests/test_attack_outcome.py`:228, and
`degrade/attacked_report.py`:179 **directly**, at `tests/test_degrade_attacked_report.py`:130;
`detector_report.py`:185 and `selective_report.py`:299 are the two. *The first edition of this
sentence put `attacked_report` in the untested bucket and explained it by saying no test enters
`eval/__main__.py` — and both halves are refuted by this row's own census, which lists neither
`attacked_report.summary_lines` nor `eval/__main__.py`'s `main` among the never-called. The
instrument was right and the prose around it was written from memory.*

**`0010` §5's loop shape was looked for, a candidate was found, and the mutation refuted it.**
`synth.overlay.PLACEMENTS` appears in `tests/` only inside self-referential products —
`len(planned) == len(PAYLOADS) * len(PLACEMENTS) * 2` at `test_attack_suite.py`:30 and twice more
in `test_degrade_attacked.py` — plus one `@pytest.mark.parametrize`, which collects nothing rather
than failing when its argument is empty. On a grep that is the shape exactly. **It is not.** Run as
§3.6 asks, in memory and touching no file: `test_attack_suite.py` collects **eleven** tests and all
eleven are green at baseline; emptying `PLACEMENTS` turns **seven red** — four failures and three
fixture errors — with `ValueError: unknown placement 'description'` / `'footer'`, because the
production constructor validates a placement against the tuple and the tests pass placement names
as **literals**. *The first edition reported "four of five", which was this session's own harness
calling test functions without their fixtures and scoring six `TypeError`s as baseline-bad — §3.6's
first observation, committed by the battery written to obey it.* And the mutation is caught
**despite** the self-referential product, not by it: `:30`'s `len(planned) == len(PAYLOADS) *
len(PLACEMENTS) * 2` is one of the four that stay green at `0 == 0`. That is a
mechanism none of the earlier three showed — `apply-scout` answers with `zip(…, strict=True)` and
`it-job-radar` with an assertion outside the loop: *a vocabulary held by a validating constructor
plus literal names in the tests is held, even when every count in sight is self-referential.* `attack.payloads.PAYLOADS` is held more conventionally, by
`test_attack_payloads.py`:77's absolute `sum(... if payload.harmless) == 1`.

*This is the third reading this session that a measurement reversed*, after the mojibake in A-4's D
and the stale branch above — and the only one of the three where the reversal cost more than a
command: the finding was drafted before the battery ran.

**And the guard's own docstring cites a commit no clone can resolve — found because this row
made the identical mistake and its review caught both.** `tests/test_site_claims.py`:8 opens
*"Two were, until `9f4bd21`"*. That SHA is a **branch** commit: this portfolio squash-merges, the
work landed on `main` as `05ed544` (#8), and `git merge-base --is-ancestor 9f4bd21 main` says no.
A reader who clones this repository has `origin/main` and nothing else, so the guard's account of
why it exists points at a commit that does not exist for them. The tree's **other** SHA citation,
`tests/test_site_committed.py`:268's `d331882`, **is** on `main` and resolves — which is what makes
this a defect rather than a policy question: the repository does it correctly once and not twice.
It is `pl-jobs-lora`'s unresolvable `ADR-0012` (A-4's axis A) in a different notation, and the index
has no instrument that can see either — `tools/citations.py` reads section references in the index's
own files, not commit SHAs in a submodule's tests.

*The observation that would have falsified this axis was run rather than written down.* The
tracer says a function was **called**, not that it is reachable, and sixteen of the twenty were
excused as CLI glue on the strength of their names. Executed instead: `python -m doc_extract.<m>
--help` answers for **all five** of `synth`, `eval`, `attack`, `foreign` and `degrade`, and
`python -m doc_extract.schema.generate_vocab --check` exits clean — which additionally says the
generated `vocab.py` has **not drifted** from the vendored schema, the one check `PROVENANCE.md`
says a re-vendor cannot skip. So the glue is reachable and `score` is the only dead function in
`src/`. What is left un-falsified is narrower: no CLI was run past `--help`, so a subcommand that
parses and then fails would not have been seen.

**B — `finding`. Two, and the first is the audit's own recurring shape arriving in a repository
that invented the cure and pointed it at the smallest patient.**

**B-5d. The guard is exemplary and it reads 153 of 820 figure-bearing lines.** `docs/index.html`
is held by **two** modules. `tests/test_site_committed.py` renders the page and byte-diffs it
against the committed file. `tests/test_site_claims.py` then does the thing no other repository in
this portfolio does: it checks the **words** around the figures — its docstring explains that the
byte-diff *"cannot establish more, because both sides of that comparison come out of
`build_index`"*, and that `apply-scout`'s `ADR-0012` *"names words as its own blind spot, so a digit
tokeniser copied across would have missed both of the defects above"*. It catches *"The **two**
payloads the arithmetic never sees"* when the list has grown to three. It also states its own
limits in the docstring rather than leaving them to be discovered. **This is the best documentation
guard the audit has seen, and A-4's B-4a is the same finding one repository over.**

*Measured, because the asymmetry is the finding and a count of pages is not one.* Taking a
substantive line to be a **distinct** line over 30 characters carrying a digit — distinct within
its own document, since a table that repeats a row is one claim maintained once:

| document | such lines | read by a test |
|---|---:|---|
| `docs/index.html` | 153 | **two modules** |
| `docs/findings.md` | 302 | no |
| `README.md` | 187 | no |
| `docs/adr/0002_placement.md` | 132 | no |
| `docs/adr/0001_trust_boundary.md` | 46 | no |
| `CLAUDE.md` | 118 | no |

**785 distinct figure-bearing lines carried by nothing, against 153 carried twice** — five times
the guarded page — by
occurrence rather than by distinct line the same rule gives 156, 303, 188, 132 and 46, and the
unit is written down here because the first edition did not write it down and the two readings
differ by three on the page — and by `CLAUDE.md`'s
own division of labour the unguarded pile is the important one: *"This file is the rules;
`docs/findings.md` is the results."* The results document is **twice** the guarded page on this
measure — and the unguarded pile as a whole is five times it — and all of it is outside the
discipline the page's guard defines. *The first edition said four times of `findings.md` alone,
which the table beside it refutes.*

*And 44 of those lines are maintained in more than one place.* Verbatim duplicates carrying a
figure, counted by document pair: **24** between `README.md` and `docs/findings.md`, **19** between
`findings.md` and `ADR-0002`, **3** between `findings.md` and `ADR-0001`, **2** between `README.md`
and `ADR-0001` — **48 pair occurrences over 44 distinct lines**, because two of them stand in three
documents and are therefore counted in three pairs.
**Two lines stand verbatim in three documents**, one of them the gate table's row
`| `high` | 20.1 % | **99.0 %** | 18 | | **65.3 %** | **99.0 %** | 18 |` at `README.md`:471,
`ADR-0001`:196 and `findings.md`:411. A correction to that row has to be made three times by hand,
and nothing would notice two.

**B-5e. Thirty-one flags the CLIs accept that no documented command line shows, and the docs never
say to ask.** The per-(package, flag) sweep: **31 undocumented, 0 wrong** — `--seed`, `--tier`,
`--per-tier`, `--limit`, `--quiet`, `--max-tokens`, `--effort`, `--rate`, `--allow-partial`,
`--placement`, `--payload`, `--rung`, `--no-verify` and more, across all five CLIs. That is the
largest count the audit has measured, against `pl-jobs-lora`'s 8 and `auth-log-scan`'s 1 — and
**seven repositories have never been examined**, so it is a running maximum and not a portfolio
one — and the
mitigating half is real: `README.md` and `CLAUDE.md` present the CLIs as a **recipe book**, a dozen
worked commands rather than a manual, which is a legitimate register. What makes it a finding
rather than a style is that **neither document mentions `--help` anywhere**, so the register is
never declared and a reader who wants a smoke run has no route to `--limit`.

**Three false positives this axis produced before it produced a finding, recorded because each is
a trap for the next session's sweep.** *First, the historical figure.* A provenance sweep flags
`20.1 %` in three documents against no artifact — and it is **correct as written**: the table is
captioned *"Left: as M7e reported it. Right: after M7g"*, so the left column is a superseded value
kept deliberately to show an inversion, exactly the practice `0008`'s errata sections ask for. Six
more of the sweep's hits are the same shape (*"before the third verdict they read 9.1 % and 7.1 %"*).
**A naive provenance guard over these documents would be wrong by design**, and that — not laziness
— may be why none exists. *Second, the plain-space separator*: `11 652` tokenises as `11` and `652`
under the separator class `pl-jobs-lora`'s page guard uses, which deliberately excludes the plain
space because it welds adjacent table cells. In prose it must be admitted; in a table it must not;
the unit decides, and this session ran the sweep twice for that reason. *Third, and it is the
instrument's own*: the flag sweep keyed on the module defining the parser, `doc_extract.eval.__main__`,
against the module the docs invoke, `doc_extract.eval`. Nothing ever matched, so it reported
**43 undocumented and 12 wrong** — both artifacts of the key. Keyed on the package it reports 31 and
0. That is the sweep's **third** scope correction after `0010` §5's two, and the first that was not
about which documents to read but about **what a CLI is called**.

*The observation that would have falsified B-5d was run rather than written down.* The claim rests
on a `git grep` for filenames, and a test reaching a document by a path built from `ROOT` without
the name as a literal would not appear in it. Asked the other way — every repo-root-relative path any test
constructs, swept on `parents[1]` as well as on the names `ROOT` and `REPO_ROOT` — they land in
exactly four places: `schemas/` (the vendored XSDs and their provenance), `src/doc_extract/`
(the fonts' provenance), `results/` and `data/scanned/`, plus `docs/index.html` and `docs/` on
`sys.path` for importing `build_index`. **No count is given here**, and that is the third
correction to this sentence: it said six, then seven, and a reviewer counting path *expressions*
rather than *destinations* gets eight. What the sweep establishes is a negative and the negative
is stable — **nothing under `docs/` but `index.html` is opened by any test** — so the claim is
written as the negative it is. The bare
`docs` is `sys.path.insert` for importing `build_index`. So nothing reaches `README.md`,
`docs/findings.md` or either ADR **by any route**, and B-5d is closed rather than probable. For
**B-5e** the open falsifier stands: `--help` was run on all five CLIs for axis A but its output was
never diffed against the parsers, so a flag the docs show under a different spelling would read as
undocumented here.

**C — `finding`, and it is in the first line of the page.** §3.3's command first:
`python -m tools.pagespec --only doc-extract` reads

> `doc-extract   clear, 3 undecided`

and exits 0. This is the richest surface the checker measures: **13 tables, every one wrapped in a
`.table-wrap` scroller**; **150 `contrast text` sites, all 150 measured, worst 5.17:1** against a
4.5:1 threshold; clause 8 satisfied with four `U+202F` and one exempt `U+00A0` specimen. And
`contrast marks` — the key that four surfaces report failing and that `0009` §7 row 12 made
report-only for exactly that reason — reads **`ok` here: 77 sites, 28 measured, worst 5.17:1
against 3.0:1**. The three undecided are `4 h1`, `1 composited` (one usage paints a value that is
not the declared one) and `contrast ground` (49 sites without a resolved ground, 3 selectors the
checker does not read).

**The finding: the page's first line contradicts two other places on the same page, and the
repository has already diagnosed the class in writing.** The eyebrow reads *"KSeF FA(3) ·
milestones 1–6 of 7, **and most of the seventh**"*. Thirty-three lines down — `docs/index.html`:175 against :208 — the caution card says
*"What exists is … **the seventh milestone's three arms** — an unfamiliar vocabulary, the page
photographed, and the attacked page photographed — **each put to a model**"*. And the table at the
foot reads *"M7 — held-out corpora, the vision path, the attacked page photographed — **built, model
arms on all three**"*. Two statements say the seventh is finished; the first line of the page says
most of it is.

*What makes this a row rather than a typo is its history, which is in the repository's own words.*
**`05ed544`** (#8) removed a `5 / 7` **"Milestones built"** KPI tile — the squash of a
four-commit branch, and the only SHA a reader can resolve. Its message says the tile was *"project
management that no artifact produces and that drifts on every milestone"*, and the generator
carries the same reasoning at `docs/build_index.py`:1578–1580, recording that the tile *"disagreed
with **this page's own eyebrow**, with the milestone table at its foot, and with the caution
card"*. The eyebrow at `build_index.py`:1838 is a hardcoded literal — `milestones 1&ndash;6 of 7,
and most of the seventh` — derived from nothing.

**And the disagreement is known and deferred on the record, which is a different finding from the
one first written here.** The same squashed commit says, in the section that added the guard:
*"Reported by the tests and **deliberately not fixed here**, because each is a **copy decision
rather than a count**: the eyebrow and the M7 table row give different verdicts on the same
milestone, both typed."* — *and the same message later withdraws half of that sentence:* **"they
were reported by the pass, not by an assertion"**. The load-bearing half survives, which is that
the deferral was judged rather than missed; what does not is the claim that a test reports it, and
that matters here because a deferral a test reports has a carrier and one a reviewer reports has
none. So it was not missed and it is not an unnoticed third turn of a wheel —
it is an open decision the repository named, deferred for a stated reason, and then published. The
finding stands on what a reader meets rather than on negligence: **the first line of a public page
contradicts two statements below it, and has since 2026-09-04.** *This row's first edition read it
as a partial fix nobody noticed. That was wrong, and it was wrong in a way the previous session's
review had already named — a chain spanning several commits credited to one — surviving a squash
that made all four messages one.*

*And the guard cannot see it, by its own account.* `tests/test_site_claims.py`'s docstring names
both surviving sites — *"The same page's eyebrow said milestones 1–6 of 7, the table at its foot
marked M3–M7 `built`"* — and then states its scope: *"It covers cardinals attached to a noun naming
a set **the repository computes**, and the four headline tiles."* Milestones are not a set the
repository computes, which is precisely why the tile had to go rather than be pinned — and it is
why the same number, in the same page's first line, is outside the guard that was written because
of it. **The repair is not to pin the eyebrow; it is to decide which of the two statements is
true and make the page say one thing.**

**What is right here, and it is most of the page.** There is a card headed *"What is not built
yet"*, opening *"Stated plainly, because a portfolio page that reads as finished when it is not is
worse than no page at all"* — and it then lists `not built` and `built in part` items against a
named milestone, including *"an adaptive attacker, which no fixed payload set stands in for"*. The
lead is the strongest opening the audit has read and every figure in it is an artifact's: *"183 798
bytes of XSD carrying 328 enumerations and **0 assertions**"*, with the first KPI tile reading `0`
because zero is the thesis. The fourth tile, `3 / 6` *"Attacks the arithmetic never sees"*, is the
one `05ed544` (#8) rebuilt after a `code-reviewer` pass blocked its predecessor for attaching a
cardinal to the wrong set — the defect class this row is about, caught in-flight by the practice
`CLAUDE.md` mandates.

*One thing the first screen costs.* It runs **135 words** before the first card — measured, and
the comparative that was first written here is withdrawn: *"the longest opening of the five
surfaces scanned so far"* did not survive being measured. By the same extractor `apply-scout`
reads **151** and `pl-jobs-lora` **120**, while `auth-log-scan` and `it-job-radar` read 1 131 and
1 463 because their pages do not use the section boundary it looks for — so three of the five are
comparable and two are the instrument talking. *A cross-surface comparison needs a reader that
finds each page's own first section, and this row does not have one.* The h1 —
*"Poland's national e-invoice schema checks nothing an accountant would"* — turns on an elided
verb. It is a good sentence and it takes a beat that a recruiter
reading five tabs may not spend. No replacement is proposed: unlike A-4's, this headline names its
own subject, carries no borrowed figure, and the elision is the only thing to trade, so the
proposal would be a style note rather than a repair.

*The observation that would falsify this axis is already closed by a test this session ran, and
naming it as open would have been wrong.* The finding assumes the eyebrow a reader sees is the
eyebrow the generator writes — and `tests/test_site_committed.py` regenerates the page and
byte-diffs it against the committed file, failing with *"docs/index.html is stale — re-run `python
docs/build_index.py`"*. It is among the 817 that passed. A scan session may not write to this
repository, so regenerating by hand was not an option; it did not need to be. **What stays open is
the opposite direction**: the checker reports `1 composited` undecided — one usage painting a value
that is not the declared one — and `contrast ground` cannot resolve a ground for 49 sites and
cannot read 3 selectors at all. Those are the checker's own gaps on the richest surface it
measures, and no reading here substitutes for them.

**D — `clear`.** `gh issue list --state all --limit 30` returns **nothing**: this repository has
never had an issue, so there is no closed-issue half to check either. `gh api .../branches` lists
exactly `main`. Both workflows are **`active`** — `.github/workflows/ci.yml` and
`dynamic/pages/pages-build-deployment` — asked of GitHub directly rather than inferred from a run
listing, which cannot distinguish a passing workflow from the only enabled one. The last runs of
both are `success`, 2026-09-09. `license` reads `mit`, matching `LICENSE` and `pyproject.toml`'s
`license = "MIT"`; `homepage` is `https://p0w3r223.github.io/doc-extract/`, which is the surface
`sources.SURFACES` reads.

*The description was read as bytes, not through the console* — §6's 2026-09-17 row, applied on its
first outing after being written. `gh api repos/… --jq .description` holds **no non-ASCII codepoint
at all**, and the sentence is accurate to the repository: *"the Ministry's schema contains zero
assertions, so every consistency rule an invoice obviously satisfies is unenforced"* is the thesis
the page leads with and the `0` the first KPI tile prints.

*One thing checked and not raised, for the third time.* **Thirteen GitHub topics against zero
`keywords` in `pyproject.toml`** — the file declares none. `apply-scout`'s `CLAUDE.md` states the
rule that would make this a defect (*"`pyproject.toml`'s `keywords` lead; the GitHub topics copy
them"*) and **this repository's `CLAUDE.md` does not carry it**, exactly as A-3 found for
`it-job-radar` and A-4 for `pl-jobs-lora`. Measured across all five, **only `apply-scout` states
it** — `auth-log-scan` lacks it too and was never checked — so it is **four of five**, which
settles what A-3 proposed and A-4 seconded: this is not a per-repository finding but one cross-repo sweep,
and the question it should ask is whether the rule was ever meant to be portfolio-wide or is
`apply-scout`'s alone.

*The observation that would have falsified this `clear` was run rather than written down, and it
is the one A-3's falsifier did not name.* `gh issue list` **excludes pull requests**, so "never had
an issue" says nothing about the tracker's other half — and a closed pull request describing code
that has since moved is exactly the `apply-scout` D-2 shape. `gh pr list --state all` answers:
**15 pull requests, every one `MERGED`**, none open and none closed-unmerged. So there is no
abandoned discussion and no rejected change whose description still stands. *What stays
unchecked:* their **bodies** were counted and not read — a scan session may read them, and this one
chose not to spend the axis there once the states came back uniform.

**A-5 errata, 2026-09-17 — fifteen corrections and one finding gained: thirteen from the
`code-reviewer` pass, two from the closing sweep below it, and the two worst refuted by this row's
own instruments.** A-4's errata
found that the battery catches what is *wrong* and a second reader catches what is *no longer right
about the thing it names*. This row tested that: the battery ran on everything and the review still
found thirteen, of which **two contradict measurements printed in the same row**.

| what it said | what it says now | how it was wrong |
|---|---|---|
| `attacked_report.summary_lines` is untested, *"called only from `eval/__main__.py`, which no test enters"* | three of five are reached; it is one of them, **directly** at `tests/test_degrade_attacked_report.py`:130 | **refuted by this row's own census**, which lists neither it nor `eval/__main__.py`'s `main` among the never-called. `tests/test_attack_outcome.py`:228 calls `eval_cli.main(["attack", …])`. The instrument was right; the prose beside it was written from memory |
| `9f4bd21` and `fae44eb`, quoted as commits | `05ed544` (#8), the squash on `main` | **branch SHAs, cited three paragraphs after this row quotes the rule against them** — `CLAUDE.md`'s *"a branch commit is never reachable from `main` and never will be"*, about this very branch. Every quotation survives: the squash's message concatenates all four |
| *"a partially applied fix… the third turn of the same wheel"* | **known, named and deferred on the record** | the squashed commit says *"Reported by the tests and **deliberately not fixed here**, because each is a **copy decision rather than a count**"*. Not an oversight — a judged deferral, which makes it a **better** finding and a different one. Second time in two sessions that a chain over several commits was credited to one |
| *"all **six** `Any` annotations are at that boundary"* | six **bare** `Any`; the tree carries `Any` 64 times in 16 modules | a count of one shape presented as a total, supporting a *"strongest codebase"* verdict |
| *"five tests green at baseline, four of five red"* | **eleven** green, **seven** red | this session's harness called test functions without their fixtures and scored six `TypeError`s as baseline-bad — **§3.6's first observation, broken by the battery written to obey it.** The conclusion strengthens: the self-referential product at `:30` is one of the four that stay green |
| the figure-bearing-line table, unit unstated | the unit is a **distinct** line; by occurrence it reads 156/303/188/132/46 | two defensible readings differing by three on the page, and the row named neither |
| *"the results document is four times the size of the guarded page"* | **twice**; the unguarded pile is four times | the row's own table, one line above, refutes it |
| *"48 of those lines"* | **44** distinct lines, **48** pair occurrences | a sum of pairwise intersections read as a count of lines; two lines stand in three documents and were counted in three pairs |
| *"`tier` is read in four places"* | **two**, `eval/detector.py`:135 and `:155` | every other `.tier` in the tree is on a different type. And the anchors were inconsistent — `tier`'s `def` is `:81`, not `:80` |
| *"the other 81 markdown files are `results/*/` reports"* | 79 reports **plus the two `PROVENANCE.md`** | against this row's own 79, and the two omitted are the documents axis E2 is built on |
| *"the answer is **six**, in full"* | **seven** — `schemas/fa3.xsd` at `tests/test_vocab.py`:17 | the sweep keyed on the names `ROOT`/`REPO_ROOT` and missed a bare `parents[1]`: **a vocabulary sweep run too narrowly, inside the paragraph claiming exhaustiveness.** B-5d's conclusion survives — no test reaches the four documents by any route |
| *"twenty-five lines down"* | thirty-three, `:175` against `:208` | a distance never measured |
| *"applied once of twice"* | *"once out of twice"* | a typo in a bolded heading |

**And one finding was gained rather than corrected, because the row committed the defect it
describes.** Citing `9f4bd21` sent this session to check whether the repository does the same — and
`tests/test_site_claims.py`:8, the docstring of its best guard, opens *"Two were, until `9f4bd21`"*,
a SHA no clone can resolve, while `tests/test_site_committed.py`:268's `d331882` is on `main` and
resolves. It is A-4's unresolvable `ADR-0012` in a different notation, and it is now in axis A.

**The closing sweep that produced this table found two more of its own, and they share a
mechanism worth naming.** Both A-4 and A-5 corrected a figure in a row body and left the **§5
bullet that repeats it** untouched: §5's README-carrier bullet still said *"48 of those lines"* and
*"constructs: six"*, and — more pointedly — §5's **census** bullet, whose entire subject is a
measured figure going stale, still credited a two-commit drop to one commit. **It then happened a
third time in the very round that recorded it**: adding `CLAUDE.md` to B-5d's table moved the
unguarded total 667 → 785 in the row and left §5 at 667. Neither was found by a
reviewer; both were found by sweeping the document for every string a correction had removed, which
takes one command and should be the last step of any errata round. *A row and the §5 bullet
derived from it are two copies of one claim, and this document has now written that finding about
four repositories while committing it twice itself.*

*What did not move: any verdict.* `E2 finding`, `A finding`, `B finding`, `C finding`, `D clear`
stand where the measurements put them, as they did across A-4's two rounds. **Three rows of this
table are the same class as A-4's** — a total that does not match its enumeration, a causal chain
credited to one commit, a vocabulary sweep run too narrowly — which is the argument for writing
these tables down rather than fixing quietly: the third occurrence is how a habit becomes visible.

**A-5 errata, round three, 2026-09-17 — the review of the whole body of work.** A second
`code-reviewer` pass read A-4 and A-5 **against each other and against the rest of this document**
rather than against their repositories, and found what the per-row passes could not: an identifier,
an ordinal, a scope, a claim of primacy. For A-5 it corrected two §-citations that resolve to real
sections with unrelated content — `0008` §3.6 is *"S3 was written and was not done"*, and `0010`
§3.3 carries no axis-A paragraph, that sentence being the scan prompt's — added `CLAUDE.md` to
B-5d's table, taking the unguarded total 667 → **785** and the ratio four times the page → five,
rescoped three superlatives from *"in the portfolio"* to *"the audit has seen"* over a sample of
five repositories in twelve, corrected `Any` to **57 across 13** as a whole word, replaced a
branch-only `fae44eb` with `05ed544` (#8), and **stopped counting the path enumeration
altogether** after it read six, then seven, and a reviewer counting path expressions got eight —
the negative it establishes is stable and the count is not.

*The same pass corrected A-4, and those corrections are not in this file.* They were made on the
archive's branch, and the copy of A-4 published here is a **third party's transplant of the
corrected archive row, with a third review round on top**. *The first edition of this paragraph
said that round had independently found several of the same defects. It had not: rounds one and
two were inherited whole, and the claim was made without the measurement that would have settled
it — seventeen corrections checked one by one against the published copy, sixteen already
present.* What round three did is two different things, and the distinction is the argument for
reviewing a transplanted row at all. It **propagated** corrections to sites the round that made
them could not see — §5 still carried a census history §4's table had already fixed, which is
`ST-3` rather than a re-finding — and it **found nine that were new**, two of them inside the
transplant paragraph its own author had written. **Not to re-check the measurements, which
reproduce**, but to sweep the sections that argue from a corrected figure. One correction of mine
reached neither and is applied by the commit carrying this line, together with the axis-B
identifier collision and the keywords tally.

*And one class survived both per-row passes and was caught only by sweeping the file.* A finding
lives in three places — the §4 row, the §5 bullet derived from it, and the session brief — and
correcting one leaves two stale. It happened three times in one day, the third inside the round
that recorded the first two. **The last step of an errata round is a sweep for every string the
round removed**, read hit by hit, because the expected count is wrong about a third of the time.

**The scan prompt's own figures for this repository reproduce exactly**, which is worth one line
because §6 exists for when they do not: *"86 markdown files and 9 321 lines, of which five hold
2 708"* — `git ls-files '*.md'` gives 86 and 9 321, and the five largest are
`docs/findings.md` 865, `README.md` 676, `ADR-0002` 482, `CLAUDE.md` 433, `ADR-0001` 252, summing
to 2 708. Those five are exactly the documents axis B measured, and the prompt's advice about the
long tail held: the other 81 are **79** `results/*/` reports, checked by re-running a
report rather than by reading prose, **plus the two `PROVENANCE.md`** that axis E2 is built on and
that were read closely. *The first edition called all 81 reports, against its own table's 79.*

**Not checked.** The **79 committed `results/*/*.md` reports** were read as an artifact *set* — for
figures, for the gate rows, for the attack leak table — and **not one was read end to end**; the
prompt says to check them by re-running a report, and no run was re-executed because every baseline
that matters costs a model call or an hour. The **attack corpus** (`attack/payloads.py`,
`suite.py`, `obey.py`) was read for its structure, its `PAYLOADS` pin and the `obey` positive
control, and **not for its payload text** — `0010` §3.1 makes this a scan precisely so it may be
read, and this session spent the budget elsewhere. `docs/findings.md`'s 865 lines were swept for
figures and read only where a figure or a table pointed into them; its **arguments are unread
prose**. The two ADRs likewise. The **committed `predictions.jsonl`** were read for identifiers
(E2) and never for their extracted free-text values. The **15 merged pull requests** were counted
by state and their bodies not read. And nothing that costs money or a GPU was run: the model arms
of M7 are taken from their committed reports.

*One thing deliberately not raised, so a repair does not find it and think it was missed.* The
local branch `fix/the-tile-counts-the-result` is four squash-merged commits that never had their
branch deleted. Deleting it is housekeeping on a developer's machine, not repository work, and it
is invisible to every clone.

### A-6 — `ab-lab`, session 6

Scanned 2026-09-17 against `portfolio-index` `9900926`, gitlink `9864e73`, entry state clean:
`ab-lab` `HEAD` identical to its `origin/main`, working tree clean. **Five axes**, E being E0 and
E2's third-party half. *The first session scanned in the published index rather than the archive*,
and one thing had to be established before axis C could mean anything: `tools/pagespec` is
**byte-identical** between the two repositories — `tools/` differs in exactly one file,
`entry_state.py`, repointed at the published home by the move — so the checker that answers below
is the one both repositories hold.

**E0 — `finding` · metadata, and it is R-1's.** Three identities and no fourth:
`P0w3r223 <p0w3r2243@gmail.com>` 102 fields, GitHub's noreply 23, and
`Piotr Cząstkiewicz <p0w3r2243@gmail.com>` 9. **9 of 67** commits, reproducing R-1's cell exactly.
The name also stands in twelve tracked files — `LICENSE` and all eleven ADR `Author:` lines —
which is the deliberate authorship A-4 recorded for the portfolio and not R-1's subject.

*This repository is the first scanned that **merges** rather than squashes*, and that changes what
a citation can do here: `main` carries `Merge pull request #10/#11/#12`, so a branch commit **is**
reachable and the unresolvable-SHA class A-5 raised has no purchase. It also produced the session's
one withdrawn finding. `git rev-list --all --not main` reads **23**, and all three release tags
resolve to commits that `git merge-base --is-ancestor` says are **not** on `main` — which reads as
three published releases orphaned from the published branch. **It is not.** Every tagged *tree* is
reproduced exactly by a commit that is on `main`: `v0.2.0`'s by `0d301bf`, `v0.3.0`'s by `f7684ef`,
`v0.4.0`'s by `bac953b`. The released code is right; only the commit objects are parallel, and
`git describe` is the only thing that suffers. *Recorded because the first reading was wrong twice:
`git merge-base --is-ancestor v0.4.0 main` compares the **annotated tag object** and always fails —
`v0.4.0^{}` is the question — and a stale `origin/` ref survived `git fetch --all`, which does not
prune, showing a remote branch `git ls-remote` says does not exist.*

**E2 — `clear`, and the corpus is arithmetic.** This is a statistics package whose data is
**simulated**: `git grep` for `read_csv`, `load_dataset`, `requests.`, `urlopen` or an `http` URL
across `src/` and `examples/` returns **nothing**, so no third party's data enters the repository at
any point. Exactly **one** committed data artifact, `docs/data/findings.json` — three keys,
`findings`, `schema_version`, `validation` — which is the record the page and the README are
generated from. No personal data, no scraped content, no licence question. *The cheapest
observation that would falsify it:* read `examples/*.py` for an embedded literal table rather than
grepping for loaders, since a pasted dataset needs no reader.

**A — `finding`, and it is the first breach of a hard ceiling the audit has measured.** **294 tests pass
and 5 deselect in 159.6 s**, `ruff check .` reports *All checks passed!* Error handling is
vacuously perfect and worth stating as such: across 12 modules there are **zero `except` clauses of
any kind**, zero `print`, and two `Any` — a closed-form numerical library that raises rather than
recovers.

**`src/ab_lab/simulate.py` is 893 lines against `good-practices.md`'s 800 maximum.** It is the only
file over 800 in the six repositories scanned so far, and it is not a near miss. *That sentence
said "in the portfolio" in this row's first edition — written into the same commit that rescopes
four such claims elsewhere in this document, and caught by the string sweep that commit's message
recommends. Six of twelve is not the portfolio, and the seventh repository is where a running
maximum stops being one.* Inside it: 31 top-level
functions and one class, the longest `clustered_ratio_draw` at 97 lines. The module's density is
the axis's second half — **14 functions exceed fifty lines across 12 modules and 3 704 lines**,
against `doc-extract`'s nine across 77 modules and 14 523. `cluster.py`:235
`cluster_robust_t_test` at 98 is the longest in the repository.

*Against that, the execution census is the best measured yet*: the stdlib call-tracer reports
**7 of 133 functions never called — 5.3 %**, and six of the seven are `results.py` properties and a
`__str__`.

**The five deselected tests were chased and they run.** `pyproject.toml`:64 sets
`addopts = "-q -m 'not slow'"`, so the documented `pytest` never runs them, and `ci.yml` runs bare
`pytest` on every push and pull request. They are not orphaned: `.github/workflows/refresh.yml`
runs `pytest -m slow -q` **weekly**, and its header explains the split — *"The cheap guards on
every pull request cannot catch that: they replay two cells at a tenth of their size… This job
re-measures everything at full size once a week."* A designed division, documented where it is
made. *Not a finding, and recorded because `0010` §3.6's second observation is that a skip is a
pass and five silent deselections on every pull request look exactly like one.*

**B — `clear`, and it is the answer two earlier rows were looking for.** `pl-jobs-lora` (B-4a) and
`doc-extract` (B-5d) both found a guarded page beside an unguarded README, and §5's bullet about
the published figure and its artifact being one `diff` apart has been asking since session 2 why
nobody takes the step. **`ab-lab` takes it.** `sitegen/build.py`:64 generates `README.md` *and*
`docs/index.html` from one record, and `tests/test_site_committed.py`'s G1 is parametrised over
`sorted(build.build())` — **every artefact the generator produces** — asserting byte-equality with
the committed file: *"a hand-edited page, README table or chart turns the pull request red."*

*And its second guard is a shape this audit has not seen.* G3 enforces an **import budget**:
`sitegen` may use the closed-form parts of `ab_lab` and may not simulate. Its docstring records why
the obvious implementation fails twice over — `from … import` binds the name before any fixture
runs, and patching `numpy.random.Generator` is a no-op because `default_rng` constructs the C-level
type directly — so the build runs in a subprocess with `default_rng` replaced, and the proof is
that `ab_lab.simulate` never entered `sys.modules`.

*What is left unguarded is small and named.* By the distinct-figure-bearing-line measure used in
A-5: `docs/index.html` 186 and `README.md` 70 are generated and byte-checked; `CLAUDE.md` (8) and
five ADRs — `0002` (16), `0004` (4), `0005` (10), `0010` (33), `0011` (25) — total **96 lines**
that no test opens. Against `doc-extract`'s 785 that is a different order of problem, and the six
other ADRs are cited by the generated documents and so travel with them.

**C — `finding`, and it is the first surface I have scanned that the checker fails.**
`python -m tools.pagespec --only ab-lab` reads

> `ab-lab   1 fail, 2 undecided`

and **exits 0**, because `contrast marks` is `report-only`. The failure is real:
**99 mark sites, 93 measured, 2 below threshold, worst 1.27:1 against 3.0:1 at a `<rect>` fill**,
with 150 outside D5's obligation of which 21 are structure paint. Everything else passes — eleven
tokens with both schemes, five tables all in `.table-wrap`, `contrast text` 44 of 44 measured at
worst 4.85:1, clause 8 satisfied with three `U+202F`. The two undecided are `4 h1` and
`contrast ground` (6 sites without a resolved ground, 1 selector unread).

*This is `CLAUDE.md`'s own sentence arriving in a row rather than in a policy block*: **a run that
prints `FAIL` and exits 0**, where the only thing saying why is the `gate policy` text. A reader of
the exit code learns nothing. The repair is a design question about two SVG marks and belongs to
`0009` §7 row 12's family, not to a repair pass on this repository.

**D — `finding`, and it is `apply-scout`'s D-2 shape four times over.** **Four issues are open and
all four are done**, each verified against the tree rather than against a claim:

| issue | asks for | in the tree |
|---|---|---|
| #1 | cluster-robust variance | `src/ab_lab/cluster.py`, exported from `__init__.py`, `ADR-0008` |
| #2 | CUPED variance reduction | `src/ab_lab/cuped.py`, exported, merged as PR #10 (v0.4.0), `ADR-0011` |
| #3 | worked e-commerce case study | `examples/ecommerce_case_study.py` |
| #4 | multiple-comparison control | `src/ab_lab/multiplicity.py`, exported, `ADR-0009` |

The README and the page both describe all four as built — *Cluster-robust*, *CUPED*,
*Benjamini-Hochberg* — so the repository contradicts its own tracker on its own front page. All
four were opened 2026-07-21 as a scoping exercise and none was closed when the work landed.
**`gh issue list --state all` returns the same four**, so there is no closed-issue half and no
tracker history to reconcile: the whole tracker is four completed items presented as open work.

*The rest of D is clean.* Description accurate and **pure ASCII**, read as bytes per §6's
2026-09-17 row; homepage set to the Pages URL; `mit` matching `LICENSE`; one branch; both
workflows `active`. **Seven topics against six `keywords`** in `pyproject.toml`, differing by
`python` alone — and this is the **first of six scanned that declares keywords at all**, which
sharpens A-5's cross-repo question: the rule `apply-scout` states is followed here without being
written down.

**Not checked.** The **eleven ADRs** were read where a figure or a citation pointed into them and
nowhere else; `0006` alone carries 94 figure-bearing lines and is unread as an argument. The
**`examples/` scripts** were read for data loaders and not executed — three of them produce the
tables the page quotes, and re-running them is the `refresh.yml` job's work rather than a scan's.
The **`slow` suite** was not run: `pytest -m slow` is the weekly job and the session ran the
default. The **failing marks** were taken from the checker's own report and never inspected in a
rendered page. And `docs/data/findings.json` was read by structure, not by value.

### A-6 errata, 2026-09-18 — two figures that do not reproduce, and a scope

Written by the stage that added `tools/queue.py`, which asks `git` the questions this row
asked and gets different answers. **The subject is identical**: `ab-lab` is still pinned at
`9864e73`, its working tree is clean, and nothing in it has moved — so this is not a page
changing under a row, which is the case §4's header protects.

**The scope.** *"This repository is the first scanned that **merges** rather than squashes"*
is true of `ab-lab` and equally true of the five scanned before it.
`git rev-list --merges --count origin/main`: `auth-log-scan` **3**, `apply-scout` **26**,
`it-job-radar` **21**, `pl-jobs-lora` **7**, `doc-extract` **4**, `ab-lab` **8** — and **24**
in this index, whose own `CLAUDE.md` says a branch commit is never reachable from `main`.
Every repository in the portfolio merged pull requests until a date between 2026-08-14 and
2026-09-03 and squashes since. What the row found is a portfolio-wide fact about a policy that
changed, and it is §6's row of 2026-09-18.

**`git rev-list --all --not main` reads 23 in the row and 0 today, and the difference is the
session's own refs.** The scan prompt's E1 sends a session to fetch `refs/pull/*/head` into
`refs/remotes/pr/*` before sweeping. With those refs fetched, the same command against the
same gitlink in a fresh clone reads **34**; with them pruned it reads **0**. A number that
moves with what the reader fetched is not a statement about the repository, and the row states
it as one — *third instance in four days of `0010` §6's environment class*, after session 3's
18 `ModuleNotFoundError` collection errors and session 4's CP1250 `gh` reading. §5 now carries
the shape.

**The three release tags are on `main`, under both conditions.**
`git merge-base --is-ancestor v0.2.0^{} main` and its two siblings all succeed, with the PR
refs fetched and without them. The row records the right question — it names `v0.4.0^{}`
against the annotated tag object as the trap its first reading fell into — and then keeps the
conclusion the wrong question produced. So *"the released code is right; only the commit
objects are parallel"* has no subject: the tagged commits **are** commits on `main`, and
`0d301bf`, `f7684ef` and `bac953b` are not reproductions of the tagged trees but, in the case
of the last two, the merge commits themselves.

**What reproduces, and it is the row's verdict.** E0's numerator: `9` commits carrying the
owner's name, which is R-1's cell for this repository. Its denominator moves with the same
refs as everything else in this paragraph — `--all` reads 44 commits in a clone with no PR
refs and `0010` §2.1 recorded 67 — so the fraction is not wrong so much as unstated. **No
verdict moves**: E0 stays `finding` · metadata and it is still R-1's.

*What this errata does not do is re-measure the row's other axes.* A, B, C and D were taken by
instruments this stage did not run, and a correction is not a re-scan.

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

### A-3 repair, 2026-09-14 — E-3, B-3 and D-3 closed, C-3 left open

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

**The two sites that are not in the tree are done too, and separately.** The GitHub
**description** lost its closing *"and browser-side DuckDB analytics over a published Parquet
artifact"* for *"and a published Parquet artifact the page is built from"*, and the topic
**`duckdb-wasm`** is gone — fourteen topics to thirteen, with `duckdb` kept, because it is a
real dependency and the build-time engine. Taken on the owner's explicit instruction and not
as part of the pull request: repository metadata is outward-facing, reversible by one command
and by no commit, so it is not something a merge can carry and not something a repair session
decides. Nothing in this index or in the sibling holds either of them — **the axis-D half of
this repository is guarded by the audit and by nothing else**, which is the same gap A-2's D
row has and is a `§5` question rather than a finding here.

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

### A-4 repair, 2026-09-18 — row 4 closed whole, in two sibling pull requests

`pl-jobs-lora` `fa26842` (#19) and `64959c4` (#20), pointer bumped in the commit carrying this
line. Entry state clean at the scan's gitlink `8fe2e02`; §3.3's command reads
`pl-jobs-lora   clear, 3 undecided` before and after. The repository's suite went **233 → 247**
and `ruff check .` stayed clean, run with `PYTHONPATH=src` in a fresh clone with no editable
install — §6's row of 2026-09-14 is why that is said rather than assumed.

**A-4.** The collector stopped folding its drops: `_fetch_examples` returns a breakdown in the
shape `build_dataset` already used, and a run prints `N urls -> M usable (F fetch failed,
U unusable page)`. `probe.dev_slice_size` and `data.sitemap_offers_sample` — the two knobs that
reach `_spread_sample`'s divisor — are validated at load instead of surfacing as a
`ZeroDivisionError` three modules away. The four untested pure functions have tests. And the
artifact the page stands on has a carrier: the report is rebuilt from the committed JSON and
required to render the committed markdown, byte for byte.

**B-4a's carrier was vacuous twice before a battery made it bite, and that is the row's most
portable result.** `tests/test_readme.py` refuses a README figure no artifact prints — and its
own docstring quotes `102.6`, `2.5` and `4.7`, the three it exists to catch, so with `tests/`
in the source corpus it sourced them to itself. The index records the identical shape in
`tools/citations.py`, whose docstring says prose about a broken citation may not write one.
Then the model-key exemption turned out to be case-sensitive: the config spells `qwen2.5-1.5b`
and `CLAUDE.md`, `ADR-0001` and the page all write `Qwen2.5-1.5B`, so three files donated a
bare `2.5` — enough to source a rounded latency cell, which is one of the three defects. Both
were found by mutation, neither by reading, and the exemption now carries a test of its own
because no mutation from outside can reach it.

**B-4b, B-4c, B-4e.** The build census came out of the README rather than being corrected. Only
one of its figures is unsourced outright — `76 %`, zero donors — and the rest are worse than
that: they resolve to something that is not their subject. `90` has four donors and `99` five,
none of them a repost count or a coverage figure; `800` has six, of which the nearest are the
*target* in `configs/config.yaml` and `ADR-0002` and the fetched count in none of them.
*The row's first edition said* **only `p90`/`p99`** *and* **twice** *— two hand counts inside a
paragraph about a hand count, corrected by the review that ran the sweep.* The HF Hub
freeze now reads as deferred on the page, in the README and in `.gitignore`, which is the
owner's call between two published sentences of which one was false. `.gitignore`'s claim about
`results/labeling_qa/` was true of `results/eval/`. And `test_docs_page.py`'s census is asserted
rather than stated — 251, 39 and 58 today against the 262, 39 and 59 it carried.

**B-4d** is the second instrument for a retired vocabulary, ported from `it-job-radar`'s
`tests/test_decisions.py` with the two changes §5 asked for: case-insensitive, because
`requirements-train.txt`'s loudest line was `COLAB-ONLY`, and **headings inside decision
documents swept while their bodies are not**. `ADR-0004`'s own headings are exempt and the
guard says so — its title and its amendment are the two places the retired name has to appear.

**C-4** took the wording the row proposed and the owner approved, with one deviation the page
itself settles: the row wrote `94 %` and the page writes `94%`, `100%` and `16%` everywhere
else, so its own typography won.

**The review round, `5ceb95b` (#21), and it is the half worth reading.** Both sibling pull
requests were merged **without** the `code-reviewer` pass `CLAUDE.md` requires before work is
proposed — recorded here rather than quietly repaired, because the pass then found six things
and one of them was load-bearing. `test_the_shipped_config_passes_both_new_validators` called
itself *"load is the assertion"* and asserted two properties of `configs/config.yaml`: deleting
**both** validator calls from `load_config` left all 247 tests green, so the clause this repair
is about — *validated at load* — had no carrier at all. The divisor also had a **third** path
neither validator can see, `--limit` from argparse, where a negative silently collects
`len(urls) - 1` offers. And the Colab sweep cited eight lines holding no marker, because it
detected over a line pair and reported the first half.

*The battery found the seventh, by doing it.* The test written for that third path was one
mutation away from **scraping production**: with the guard removed it went through `_session`
into a live fetch of `theprotocol.it` and ran ten minutes before it was killed. It now replaces
the session with a refusal, so it asserts the order rather than only the raise.

*What this repair did not touch.* The notebook, the two ADRs read as arguments, and the report's
rows end to end — §4's `Not checked` cell for this row still holds, and closing a finding is not
re-scanning the repository.

### A-5 repair, 2026-09-18 — row 5 closed whole, and an id that held two findings

`doc-extract` `e9e2c22` (#16), pointer moved from `7ae9c84` in the commit carrying this line.
Entry state: the index level with its `origin/main`, and `doc-extract` `HEAD`, its `origin/main`
and the index's gitlink all `7ae9c84`, working tree clean. §3.3's command reads
`clear, 3 undecided` at both gitlinks, the same three keys either side. The
repository's suite went **800 → 802**, 34 skipped at both, run with `PYTHONPATH=src` in a fresh
clone with no editable install and no `data/`; `ruff check .` clean. On this side 666 pass, the
gate exits 0, and `tools.citations` reports nothing unresolved.

**A-5 holds two findings and one id, and that is this row's most portable result.** The first is
the one the row labels: `eval/scorer.py`'s `score` was a wrapper forwarding to `judge` that
nothing called — nine modules import from that module and every import pulls something else, and
`ruff` cannot see it, because an unused module-level function is not an unused import. It is gone,
with a comment standing where it was naming `judge` as the entry point; the evaluation CLI's
`score` subcommand is a different function in a different module and is untouched. The finding was
never the dead line but where it sat.

**The second is unlabelled, and it is why §6 gained a rule on the same day.** A guard's docstring
cited `9f4bd21`, which `git cat-file -t` rejects in every clone; it cites `05ed544` now, verified
an ancestor of `main`. A suffixed id is only minted when a second finding on an axis needs one, so
this one lived under the bare row id and was invisible to a session reading §4's `Open` column —
which closed `A-5` over it and **pushed the row**, while the resolvable SHA for the very same
commit sat in that session's own C-5 commit body. Caught by a `code-reviewer` pass that re-read
the audit section rather than the diff, which is the one reading that can see an item the diff
never mentions.

**E-5a.** The vendored font `LICENSE` was the one pinned file the artifacts guard excluded, on the
reasoning that it bears on no rendered byte or parsed schema — true, and the wrong test, because
the licence requires its notice to travel with the fonts. Measured before repairing: deleting the
file left both tests green. The repair then carried a second defect and caught it — `declared()`
recomputed the directory downstream from the extension, which was correct only while the one
extensionless file was excluded, so adding it under that rule would have reported the file missing
rather than wrong. `declared()` carries the path now, and both branches were proven red.

**E-5b.** `schemas/PROVENANCE.md` recorded source, publisher, dates, digest and the complete import
closure, and said nothing about terms — for 268 kB of ministry XSD sitting under a root `LICENSE`
granting MIT over the tree. It carries a `Licence` row now, with Article 4 of the Polish copyright
act written down as a reading rather than as settled law, and explicit that it is **not** a grant
and **not** MIT. The carve-out had lived only in prose while every automated reader saw MIT, so
`LICENSE` gained a *Third-party components* section naming both directories.

**E-5c.** `synth/pools.py` called *no real taxpayer appears in the corpus* a requirement rather
than a courtesy, on provenance alone — and *not copied from a register* cannot establish *not in
one*. The line below it showed the author knew the difference, because the IBANs use bank prefixes
drawn from ranges no bank uses. Recomputed here by residue DP over `_NIP_WEIGHTS`: **810 000 001**
constructible values against 891 000 000 shape-valid prefixes. The docstring now says that, says
what a collision costs — a NIP is public business data, so it identifies no person — and says what
would fix it. **Whether a prefix range assigned to no tax office exists is not answered**, because
inventing one would replace a measured overclaim with an unmeasured one.

**B-5d.** Most of the 785-against-153 gap is not closable — a figure sourced to a committed run
cannot be checked without re-deriving the run — but one part of it is mechanical, and it is the
part that has actually gone wrong across this portfolio: the same claim written into two
documents, corrected in one, left stale in the other. There is a guard now, and it is the whole of
the suite's **+2**: the check, and its own vacuity test. It sources no figure to itself — it
asserts only that where two documents say almost the same thing they say the same numbers — so it
cannot go vacuous by quoting the values it checks, which is how a sibling's README guard was
vacuous twice. Three traps are kept in the module because each caught it: the unit is a passage
and not a line, since comparing hard-wrapped lines measures the wrapping; the rule is a conflict
and not an inequality, since one document declining to state a count is an omission; and
`difflib`'s `autojunk` applies to `seq2` only, so the verdict moved with argument order until it
was turned off.

**B-5e.** The recipe-book register is legitimate, is kept, and is now **declared**, with `--help`
named in both documents the row said were silent about it — verified on all five CLIs and per
subcommand. **No count is published.** The audit's 31 is a per-`(package, flag)` pair count; the
README restated it as accepted flags and then subtracted names from pairs. Every sweep run at
this population has returned its own answer, because the key is a choice none of them stated —
flag name or pair, one document or two, subcommand parsers enumerated or not. **No number of
sweeps is given here either**: `README.md` says three and does not count the review pass that
caught its own restatement, which is the disagreement a reader would otherwise find between two
documents and have no way to settle. The count of flags stays in the audit, which is where the
unit is written down.

**C-5.** The page's first line stops carrying a fraction. It reads *what is not built is named at
the foot of this page* — true, pointing at a generated table, and unable to drift. The repair
follows the repository's own reasoning rather than picking a winner: `05ed544` deleted a `5 / 7`
KPI tile from this same page for being a hardcoded fraction derived from nothing, and the eyebrow
was that defect one element over. **Deliberately not adjudicated: whether the seventh milestone is
finished.** The table and the README disagree, it is a copy decision and not a measurement, and
the new wording is true under either.

**And the substitution was applied to the generator and to the page rather than regenerated.**
`python docs/build_index.py` in a fresh clone deletes 64 lines of the published page: the
corpus-dependent blocks need `data/scanned/`, and `data/` is 116 MB and gitignored, so no clone
has it and neither does CI. The page's byte-diff guard strips exactly those blocks before
comparing — a one-directional allowance the workflow documents — so a blind rebuild is green,
reviews clean, and quietly unpublishes a measurement. §6's row of the same date is the rule this
cost, and it was found by running the generator rather than by reading it.

**And this row was `pending` for the length of a review without the word ever being written.**
§4 defines the state as *the repair exists and is not on `main` yet: an open pull request, or a
pointer not bumped* — which is exactly what stood between `843081d` and this commit, while the
cells read `closed`. That is a second defect of that push, different from the one §6 already
records. **No instrument objected, and one of them looked**: `sibling_citations()` verdicts a
cited commit against the *submodule's* `origin/main` and never against the gitlink the index
pins, so a commit merged in the sibling and not yet pointed at reads `on main`.

**Closed one commit later, in this same pull request.** `sibling_citations()` asks the gitlink as
well and answers `beyond the gitlink`; `unpinned_closures()` pairs that verdict with a row whose
cells claim no open work, which is the shape this repair arrived as. Printed by the module and
**refused** by `tests/test_queue.py` — the split the census's own docstring argues for, and it
survives that argument: adjacency can misattribute a line and therefore cannot gate, but *the
pointer is either bumped or it is not* is true whichever row the citation belongs to.

**Where that refusal happens, because the sentence above is not a claim about the build.** The
state assertion over §4's real rows reads the sibling working trees, so `core` deselects it and
`surfaces` and `live` check out shallow and skip it: **no CI job runs it**, and it refuses in a
working session — which is the position `sibling_citations()` already argues for itself, and
changing it would buy the adjacency heuristic a job. The *pairing* underneath it needs no git
and does run in `core`, which is where the logic is actually held. Found by the review of this
stage, over a first draft that said `refused` and left a reader to assume CI. §4's
*`declined` and `pending` have no instance today* still holds literally, no cell having carried
the word.

*What this repair did not touch.* R-1 stays deferred, here as everywhere. §4's `Not checked` cell
for this row still holds — the 79 result reports end to end, the attack payload text,
`findings.md` as an argument, and the merged pull request bodies — and closing eight findings
under seven ids is not re-scanning the repository.

### A-6 repair, 2026-09-18 — D-6 closed, C-6 deferred, A-6 measured and left open

Entry state: `ab-lab` `HEAD`, its `origin/main` and the index's gitlink are all `9864e73`, the
working tree clean. §3.3's command before and after reads `ab-lab   1 fail, 2 undecided` — the
`contrast marks` failure A-6 recorded, unchanged, because **this pass edits no file in
`ab-lab`**.

**A-6 stays `open`, and the reason the plan gave for closing it does not survive a
measurement.** The architecture pass that opened this phase recommended `declined` on the
grounds that a closed-form numerical library has no boundary to split on. It has three, and
they are written in the module's own docstrings: **seven** draws — `binary_draw` through
`covariate_draw`, **308** lines — ten **adapters** of 3 to 14 lines, nine of them opening
*"Adapter: …"* and the tenth *"Adapter factory: …"*, and seven **runners**
(`run_experiments`, `run_clustered_experiments`, `run_metric_suite`, `run_with_peeking`,
`peeking_curve` and two more). *This read* **eight draws, about 290 lines** *in the first
edition — a hand count inside the sentence that says the boundary comes from the module's own
docstrings, found by the review. The eighth was `poisson_cluster_size`, which returns a
function that gives cluster sizes and draws no experiment.* Re-measured here rather than
carried from the row, **every size figure the split rests on reproduces**: `simulate.py`
**893** lines against `good-practices.md`'s 800, 31 top-level functions and one class, longest
`clustered_ratio_draw` at **97**, and **14** functions over fifty across 12 modules and
**3 704** lines. *Only those.* A-6's A axis also carries a test count, a `ruff` run, a wall
time and an execution census, and this pass re-ran none of them — §4's errata above says as
much about the other axes and the same holds inside this one.

So the finding is real and the refusal would have been false — **`SC-1`**, a planned item
costed from a description that is wrong about what is there, arriving against a plan this
session commissioned itself. What A-6 is instead is
**second-column work** under §3.5: a new module is outside a one-pass repair by definition, and
here the blast radius is not the module. `sitegen/build.py` generates `README.md` and
`docs/index.html` from one record, G1 byte-checks every artefact the generator produces, and G3
proves an import budget in a subprocess. *Two things the stage that takes it need not
re-derive.* **G3 refuses on the exact string `ab_lab.simulate`** — `tests/test_site_committed.py`
prints every `ab_lab*` name the subprocess imported and then asserts that one is not among them
— so a `simulate/` **package keeping that name** leaves the guard biting, because importing
`ab_lab.simulate.draws` puts `ab_lab.simulate` in `sys.modules` exactly as the module does.
**Renaming it anywhere else leaves G3 green over nothing**: the assertion is a literal, so a package called `ab_lab/sim/` makes it trivially true. That is `SG-2`'s shape reached from the naming side rather than from a tool's default — the assertion stays correct, and its answer is always the one it wants. *The first edition
of this note said the guard reads names beginning `ab_lab`; that describes the line that
prints the probe, not the line that refuses, and the difference is the whole value of the note
to its reader.*

**And the boundary is not where a split would naturally cut.** The module is laid out by
mechanism rather than by type: `clustered_ratio_draw` is followed by its two adapters and then
`run_ratio_experiments`, `covariate_draw` by `cuped_test`, `unadjusted_test` and
`run_cuped_experiments`, and so on — which is why `covariate_draw` sits after the ratio
adapters instead of beside the other draws. So draws / adapters / runners is a split **by
type**, and `good-practices.md` §1, the same file this row quotes for the 800-line ceiling,
asks for feature or domain instead. Both readings are recorded because the stage that takes
A-6 has to choose between them, and neither is derivable from a line count.

**C-6 → `deferred`.** Two `<rect>` marks at 1.27:1 against 3.0:1 under a `report-only` key.
A-6 already routes it: this is `0009` §7 row 12's family and a design question about what a
mark drawn on another mark is worth, not a repair pass on this repository. Nothing a session
may do closes it, which is what the state word says.

**D-6 → `closed`, on the owner's explicit instruction, and the sequence is the point.** Four
issues were open and all four were done. This pass re-checked the artefacts against the tree
rather than against the row — `src/ab_lab/cluster.py`, `src/ab_lab/cuped.py`,
`src/ab_lab/multiplicity.py` and `examples/ecommerce_case_study.py`, with twelve lines in
`__init__.py` naming them, and `gh` returning the same four numbers and titles A-6 recorded.
Then it **stopped and asked**, because closing an issue is outward-facing, and it acted when
the instruction came: `ab-lab` #1, #2, #3 and #4 closed 2026-09-18, each with a comment naming
the file that answers it and, **where one exists**, the ADR that decided it — #3's does not,
because the worked case study has no ADR and A-6's own table says so. `gh issue list --state all` now returns
four `CLOSED` and nothing open, so the repository has stopped contradicting its own tracker on
its own front page.

**No file changed and no pull request exists**, which is why this closure cites issue numbers
rather than a commit on `main`: the whole repair lives in GitHub state. Two things follow that
a later reader should not have to re-derive. **It needed no issue body** — the row was the
source, which is `0010` §3.1's scan/repair split doing exactly what it was built for, and the
counter-example is `D-2`, still `deferred`, where the repair *is* an edit to the bodies.
And **the precedent that shaped the pause is §4's A-3 repair**, where this repository's own
metadata moved only on an explicit instruction. The standing reminder that reasoning past a
rule to reach an easy action is the practice `CLAUDE.md` forbids by name is **§6's repair row
of 2026-09-14** — the one about `D-2`'s issue bodies, not its sibling of the same date, which
is about a bare `pytest` in session 3.

## 5. Cross-cutting

What recurred rather than happened once. A per-repository split cannot see a pattern by
construction; this section and §2's baselines are where patterns accumulate.

- **§2.3, E1 across all thirteen: clean.** Sweeping once rather than thirteen times is what
  made the three matches cheap to read together and dismiss together.
- **A flag the CLI accepts and no document names — and the shape has a second half nobody had
  measured.** *No count stands in this lead, on purpose.* Every session so far has added an
  instance, and the lead said *three repositories, three sessions* while the paragraph appended
  directly under it documented a fourth — `pl-jobs-lora`'s `--candidates`, named in no document
  at all. A lead figure in a bullet the queue keeps extending is stale by the next session and
  is read by everyone who quotes the shape; the instances below are the count. `auth-log-scan`'s
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
  **Fourth repository, and the instrument's second new occurrence — this time on a flag
  defined twice.** `pl-jobs-lora` (A-4): `probe.py`'s `--candidates` is named in no document at
  all, and `--fresh` is defined by **both** `inference/predict_gguf.py`:141 and
  `inference/predict_hf.py`:207 while `README.md`:220 shows it under `predict_gguf` only. That
  is the *wrong-subcommand* half arriving in a new form: not a flag credited to the wrong
  sibling, but one genuinely documented for a module and silently missing for a **second module
  that defines it too** — and the missing one is the **hosted-GPU** entrypoint, where re-running
  is the expensive operation the flag controls. The sweep needed no adaptation to find it, which
  is three trees in three sessions on one instrument.
  **Fifth repository, the largest count the audit has measured, and the sweep's third scope
  correction — this one about what a CLI is *called*.** `doc-extract` (A-5): **31** flags defined
  and shown in no documented command line, `0` wrong, across five CLIs. The mitigating half is
  that its documents teach the CLIs as a recipe book rather than a manual, which is a legitimate
  register; what makes it a finding anyway is that **neither mentions `--help`**, so the register
  is never declared. The correction: those CLIs are `__main__.py` inside a package, invoked as
  `python -m doc_extract.eval`, and the sweep keyed on the module defining the parser,
  `doc_extract.eval.__main__`. **Nothing matched in either direction**, so it reported 43
  undocumented *and* 12 wrong — two plausible figures, both artifacts of the key. Keyed on the
  package: 31 and 0. Add to the specification: **key on the name the documentation invokes**, and
  treat a sweep that reports errors in both directions at once as an instrument fault until proven
  otherwise.
  **Closed 2026-09-18 at `doc-extract` `e9e2c22`, and the mitigating half is what survived.**
  The register was declared rather than converted to a manual: `README.md` and `CLAUDE.md` both
  name `--help` now, so *neither mentions it* reads as of the scan and not as of today. The
  **31** stays in this bullet because this is where its unit is written down — a
  per-`(package, flag)` pair count — and the repair deliberately publishes no figure, having
  watched this one restated as a count of flags in the sibling's own README and caught in
  review.
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
  **Session 6 answers it.** `ab-lab` (B in A-6) **generates the README**: `sitegen/build.py`:64
  writes `README.md` and `docs/index.html` from one record, and `tests/test_site_committed.py`'s
  G1 is parametrised over *every artefact the generator produces*, asserting byte-equality — *"a
  hand-edited page, README table or chart turns the pull request red."* The step this bullet has
  asked about since session 2 costs one `parametrize` over the build's own output, and the
  repository that took it stopped treating the README as prose beside a generated page and started
  treating it as a second output of one build. **That reframes the bullet for the repositories
  still in the queue**: the question is not *is the README checked* but *is it generated*, because
  a README nobody hand-edits needs no provenance guard at all.
  *And its second guard is a shape this audit has no other instance of.* G3 enforces an **import
  budget** — `sitegen` may use the closed-form parts of `ab_lab` and may not simulate — in a
  subprocess with `numpy.random.default_rng` replaced, proving the constraint by
  `ab_lab.simulate` never entering `sys.modules`. Its docstring records the two in-process versions
  that silently do not work: a top-level `from … import` binds the name before any fixture runs,
  and patching `numpy.random.Generator` is a no-op because `default_rng` constructs the C-level
  type directly.
  **Closed 2026-09-18, and the close is a counter-example to the reframing above.** `ab-lab`
  answered *generate the README*; `pl-jobs-lora` took the other route and had it **checked** —
  `tests/test_readme.py`, `0007` §5.0 over the second surface, reusing the page guard's own
  `_canonical` and `_NUMBER`. Both close the bullet and they are not the same answer: a
  generated README cannot drift and needs no provenance guard, a checked one can and does, and
  the choice belongs to whether the document is an output of a build or a thing a person
  writes. *So the question is not only* **is the README generated** *— it is which of the two a
  repository is willing to be.* The fifth repository's carrier also went vacuous twice before a
  mutation made it bite, which is in `0010` §4's A-4 repair and is the cheaper half to copy.
  **Third repository, and the sharpest form yet: the repository said the README was a surface,
  in a commit title, and did not extend the carrier.** `pl-jobs-lora` (B-4a) holds
  `tests/test_docs_page.py`, 327 lines enforcing `0007` §5.0 over `docs/index.html` — and the
  README reproduces the same evaluation table with **three cells rounded away** from what
  `results/eval/report.md` prints. The commit that corrected four *other* cells of that table,
  `305f4e2`, is titled *"the README is a surface too, and the guard was stricter than the
  spec"*: it acted on the first clause by hand and left the second clause's machinery pointed
  where it already was. **A hand pass over a table is a hand count**, and this portfolio's hand
  counts have read 15, 18 and 19 against a true 20. What makes it worth a sweep rather than a
  row is that the carrier here is not merely nearby — it is in the same directory, imports
  cleanly, and this session reused its `_canonical` and `_NUMBER` against the README in nine
  lines. The question to ask of every repository with a page guard is simply *what else does
  this repository publish that the guard does not read*.
  **Fourth repository, and it inverts the bullet's own assumption: the guard there is the best the
  audit has seen and it reads the smallest of the five documents.** `doc-extract` (B-5d) holds
  `tests/test_site_claims.py`, which checks the **words** around the figures — it catches *"The
  **two** payloads the arithmetic never sees"* when the computed list has grown to three, a defect
  every digit tokeniser in this portfolio would pass — and states its own scope limits in its
  docstring. It reads `docs/index.html`'s **153** distinct figure-bearing lines.
  `docs/findings.md` (302), `README.md` (187), two ADRs (178) and `CLAUDE.md` (118) — **785
  lines**, five times the guarded page — are reached by **no test by any route**, established by
  sweeping every repo-root-relative path any test constructs. **44 of those lines stand verbatim
  in more than one document**, over 48 document-pair occurrences, two of them in three documents.
  **And there is a reason not to simply extend the guard, which this bullet did not previously
  have.** Those documents deliberately keep superseded figures — a gate table captioned *"Left: as
  M7e reported it. Right: after M7g"* — so a provenance guard of the kind `pl-jobs-lora` needs
  would be **wrong by design** there, reddening on the repository's own errata practice.
  **Closed 2026-09-18 at `doc-extract` `e9e2c22`, and the repair answers this objection rather
  than working around it.** What was added is not a provenance guard: it asserts that where two
  documents say almost the same thing they say the same numbers, which is immune to
  deliberately superseded figures by construction — a retired figure and its replacement do not
  stand in near-identical passages, they stand in a table that contrasts them. So *reached by
  no test by any route* is no longer true of the five documents: all five are read. **It is
  still true of most of the 785 lines**, because the guard checks documents against each other
  and not a line against the artifact behind it, which is the half `pl-jobs-lora` needs and
  this repository still does not have.
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
  **Second occurrence, and it moves the shape from *watch* to *rule* — with the amendment's own
  wording as the mechanism.** `pl-jobs-lora` (B-4): `ADR-0004`'s 2026-08-21 amendment retired
  Colab for Kaggle and wrote *"The docstrings and README that said 'Colab' now say hosted
  GPU"* — a sentence that is **true**, and that names the two classes it fixed. Fifteen lines in
  neither class still say Colab: `pyproject.toml`:17 and :60, `.github/workflows/ci.yml`:16,
  `.gitignore`:9, `configs/config.yaml`:87 and :98, `requirements-train.txt`:1, :4 and :5, and
  six more across `ADR-0003` and `ADR-0006`, the last of them a step heading. **Run the sweep
  case-insensitively**: `git grep -c 'Colab'` misses `requirements-train.txt`:1's `COLAB-ONLY`,
  which is the loudest line in that file, and a retired vocabulary is exactly the thing a tree
  spells inconsistently. So the two instances differ in
  exactly the way that matters for the sweep: `it-job-radar`'s fan-out reached GitHub metadata,
  which no commit carries, while this one reached **packaging, CI and the ignore file**, which a
  commit carries perfectly. And the mechanism is now visible — *naming the classes you fixed
  reads, to the next reader, as naming all the classes there are*, so the sweep must be run by
  an instrument against the retired vocabulary and never inferred from the amendment's prose.
  The exclusion list above needs one amendment of its own: `docs/adr` is outside the sweep
  because a dated record should still read as written, but a **step heading a reader follows** —
  `ADR-0006`:104's `## Colab Step 0` — is a manual wearing an ADR's number.
- **A census that came from an instrument, frozen into prose four lines from the instrument.**
  `pl-jobs-lora`'s `tests/test_docs_page.py` states its own limit honestly — *"262 figures
  admitted, 39 of them bare one- or two-digit integers"* — and that is **exactly right at the
  commit that wrote it**, reproduced here by running the same tokeniser against the same four
  artifacts at `879b5df`. It went stale over **two** commits with two unrelated causes:
  `305f4e2` added `_canonical`, folding ten trailing-zero duplicates to 252, and `36524c4`'s
  `Author:` migration then took the figure `223` out of the artifact set, leaving 251.
  *This bullet credited both to one commit until the review of the transplant. §4's errata had
  already corrected that exact sentence, and the correction was not carried into the section a
  reader comes to for patterns — `ST-3`, in the bullet arguing that a census goes stale four
  lines from the instrument that produces it. The arithmetic said so unaided: 262 − 10 is 252.*
  Distinct from every
  other figure defect this audit has collected, because nothing was hand-counted and nothing
  was careless — the number was measured, correctly, and then the definition underneath it
  moved. The `39` survives, which is the tell: a bare integer has no trailing zero to fold, so
  half the sentence is still true and the half that is not looks identical. **The remedy is one
  line and it is already the repository's own house style**: assert the census instead of
  stating it, so the commit that changes what a figure means cannot land green. `0008` §4.11
  and `0007` §3 are the same lesson from the other end — there, a measurement in a normative
  document; here, a measurement in a comment attached to the code that produces it, which is the
  place it is *least* expected to rot. **And the class is not the repositories' alone**:
  `0010` A-4's own errata records six hand counts inside the row that raised this bullet,
  found by its closing review before it was proposed as merged work. A rule that has to be
  applied to prose by the person writing the prose is a rule with no carrier, here as much as
  in any tree the audit judges.
- **A defect the repository diagnosed, named, deferred with a reason, and published — and the
  deferral has no carrier, so on the page it is indistinguishable from an oversight.**
  `doc-extract` (C in A-5): the page's first line says *"milestones 1–6 of 7, and most of the
  seventh"* while the caution card and the milestone table below it both say the seventh is built
  with all three arms put to a model. `05ed544` (#8) removed a KPI tile carrying the same claim,
  and the same squashed commit says of this pair: *"Reported by the tests and **deliberately not
  fixed here**, because each is a **copy decision rather than a count**"* — later withdrawing half
  of that sentence, *"they were reported by the pass, not by an assertion"*. So it was seen, judged
  out of scope for a counting fix, and shipped. **That is a defensible call and it leaves a public
  page contradicting itself in its first line since 2026-09-04**, because a deferral recorded in a
  commit message is read by nobody who reads the page.
  **The instrument this asks for is not a sweep but a ledger.** A repository that defers a named
  defect in a commit message has no place that still says so afterwards — `0008` is the index's
  answer to the same problem and no submodule has one. The cheap version is a test: when a commit
  says *deliberately not fixed*, pin the thing it declined to fix, so the deferral fails loudly if
  someone later assumes it was done.
  **Closed 2026-09-18 at `doc-extract` `e9e2c22` — the contradiction, not the defect this
  bullet is about.** The eyebrow stopped carrying the fraction, so the page no longer disagrees
  with itself in its first line. The repair did not adjudicate the milestone and said so, which
  leaves the deferral recorded in prose and in a commit message exactly as this bullet
  describes: **the ledger it asks for still exists in no submodule.**
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

- **An instrument whose answer is about the reader's environment rather than about the
  subject, and the third instance is the one that makes it a rule.** Session 3's bare `pytest`
  produced 18 `ModuleNotFoundError` collection errors that read exactly like §3.4's `blocked`;
  session 4's `gh repo view` through a CP1250 console produced mojibake on a repository's front
  door and was written up as a D finding before it was withdrawn; and session 6's
  `git rev-list --all` produced a count of commits *"orphaned from the published branch"* that
  is **0** in a clone with no PR refs and **34** in one that ran the scan prompt's own E1
  fetch. The first two are §6 rows because they indict a repository; this one is different in a
  way worth keeping: **the prompt creates the condition**, in a step four sections above the
  one that quotes the number. So the rule is not *check your environment* — it is that a
  command whose result set is `--all`, `--remotes` or any glob over refs is reporting on a
  clone, and the figure has to name the ref set beside it or ask a named ref instead.
  `0010` R-1's denominators and §2.1's commit column are both `--all` readings, which is why
  this belongs here rather than in one row's errata.

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
| 2026-09-10 | **v2.0**, as a warning and not a contradiction | §2.2's surface baseline was measured at `a9c3912`, about an hour before S14b gave `contrast marks` a verdict; a session quoting it would write `clear` into a row where its own run prints `1 fail`, with the `undecided` counts moved too | §2.2's erratum — axis C quotes the run the session made, and the key is `report-only`, which is why the gate still exits 0. **No count is given here on purpose**: this cell said *five of the eleven* until 2026-09-11 and was stale within hours of being written, because `ADR-0008` §10 took the marks census 88 → 26 the same evening and `it-job-radar` went clean. A warning about what a session's own run prints must not carry a figure the session's own run contradicts |
| 2026-09-17 | **v3.0**, scan | the prompt sends axis D to `gh` and says nothing about how its output is read. In this environment `gh repo view --json … ` piped through the console renders a UTF-8 `×` as `Ă—` — a CP1250 round trip — so `pl-jobs-lora`'s repository description read as mojibake **on its front door, twice**, and was written up as a D finding before it was withdrawn | **An instrument's own encoding is part of the instrument.** Re-take any non-ASCII `gh` reading as bytes — `gh api repos/… --jq .description` to a file, decoded explicitly — before it becomes a finding; fetched that way the description holds one `U+00D7` and is correct. Second instance in two sessions of one class: session 3's 18 `ModuleNotFoundError` collection errors were an environment verdict too, and §6's 2026-09-14 row is its sibling. *The generalisation both rows share: a reading that indicts a repository has to survive being re-taken by a second route before it is written down* |
| 2026-09-17 | **v3.0**, both prompts | §3.1's session 13 and §3.3's command row named `current_projects` as the repository a session branches and commits in — and `0011` §6 route A made it the archive that same day, where a commit reaches no reader at all. *The prompts' own text is clean and they are bound anyway*: `git grep -c current_projects` over both returns zero, for two different reasons — the scan prompt names the **role** (*"the index audit branch"*, *"in the index"*), which moved with the route, and the repair prompt never names the index at all, saying *"this repository"*. So a session reading only a prompt is not misled and a session reading the queue is, which is why the correction lives here. **Session 4 is the worked instance**: it was scanned, reviewed and twice errata'd on a branch in a repository that by evening accepted no commits, and it reached a reader only by transplant | **The index is `P0w3r223/portfolio-index`**, and that is where a session branches, commits, and opens its pull request. The archive is outside the queue and outside the corpus: `0011` is its audit of record — every blob in its object database and 533 commits across every ref, which no scan session can better — §3.1's note carries the reasoning, and **the denominator stays fifteen**. A session that finds an unpushed branch in the archive should read `0012` §4 before doing anything with it: route A rewrote no history, so the branch's base survives under the same SHA and a cherry-pick applies, and two commands settle in advance whether it can conflict |
| 2026-09-18 | **v2.0**, repair, and `CLAUDE.md`'s entry-state section | the closing rule sends a session to cite the commit **on `main`** and gives one reason for it — *“this repository squash-merges, so a branch SHA exists for no later reader”*. The reason is true of this repository **today** and false of its history, and false of all twelve siblings' too: `git rev-list --merges --count origin/main` reads **24** here and between **1 and 26** in every one of the twelve. Every repository in the portfolio merged its pull requests until some date between 2026-08-14 and 2026-09-03 and has squashed since, so a branch commit from that era is reachable from `main` permanently. `0010` A-6 built a finding on the same premise read the other way round, and its errata is in §4 | **Cite what a reader can resolve, and ask rather than remember.** `git merge-base --is-ancestor <sha> origin/main` answers it in one command per repository, and `python -m tools.queue` now asks it of every `Index SHA` in §4 and prints the sibling commits the rows cite. What the rule asks for does not change — everything committed since 2026-09-03 is squashed and a branch SHA written today resolves for nobody — but its reason is a policy with a date on it rather than a property of the repository, and a session that knows which is which can check |
| 2026-09-18 | **v2.0**, repair | closing step 1 reads *“Set the row's state to `closed` … and cite the commit **on `main`**”*, and assumes a repair always produces one. `D-6`'s repair is four issues closed on GitHub: it changes no file, so there is no commit to cite and no pull request to open, and a session following the step literally either invents a citation or leaves a done row `open`. §4's own definition of `closed` had the same gap and is amended in the same commit | **Cite the outward artefact instead, and say that is what you are doing.** Issue numbers with their closing date, or the metadata field and its new value — whatever a reader can resolve without this repository. The commit rule is unchanged wherever a file moves, which is every other closure in §4 so far. *`D-3`'s repair of 2026-09-14 was half this shape and did not raise it, because the other half carried a commit and the row read as normal* |
| 2026-09-18 | **v2.0**, repair | nothing in the prompt asks what a generator's **inputs** are before running it. Closing `C-5` meant changing a literal in `doc-extract`'s `docs/build_index.py`, and the obvious next step — run the generator, commit the page — **deletes 64 lines of the published page** in any checkout without `data/scanned/`. `data/` is 116 MB, is a function of one seed, and is gitignored, so no clone has it and neither does CI. The page's own byte-diff guard cannot catch it: `test_site_committed.py` strips exactly those corpus-dependent blocks before comparing, an allowance the CI workflow documents as deliberate and one-directional. A blind rebuild is green, reviews clean, and quietly unpublishes a measurement | **Before regenerating any artifact, run the generator on an unmodified tree and diff its output against the committed file.** A non-empty diff there means the checkout is missing an input and the generator is not safe to commit from; apply the change as the identical substitution to the generator *and* to its output instead, and let the guard confirm the two agree. The trap generalises past this repository — `ab-lab` generates its `README.md` as well as its page, and `wroclaw-air-insights` commits no page at all — and `CLAUDE.md`'s *"do not commit a page from here"* does not cover it, because that rule is about the index editing a sibling rather than about a sibling's own build. *Found by running it rather than by reading: the diff was inspected only because the tree came back dirty after a rebuild expected to be a no-op* |
| 2026-09-18 | **v2.0**, repair, and §4's `Open` vocabulary | **an id is not a finding, and closing step 1 treats them as the same thing.** `A-5` names *two* bolded findings — the dead `score`, and a guard whose docstring cites `9f4bd21`, a commit `git cat-file -t` rejects in every clone. Only the first is labelled, because a suffixed id is only minted when a second finding on an axis needs one, so the second lives under the bare row id and is invisible to a session working from §4's `Open` column. This session repaired the first, wrote `A-5 closed` into the row, and **pushed it** — the row was wrong on the remote for the length of a review, and the resolvable SHA for the very same commit was sitting in that session's own C-5 commit body while the file went untouched | **Before writing `closed`, re-read the item's section and count the bolded findings in it.** The `Open` column is an index, not an inventory: `A-5`, `A-6` and every unsuffixed id can hold more than one. Where a section holds two, close both or write the state as partial and name what is left. *The generalisation this shares with the row above: both were caught by a `code-reviewer` pass that re-read the audit section rather than the diff, which is the one reading that can see an item the diff never mentions* |
