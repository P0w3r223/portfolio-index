# Portfolio audit — SCAN session                                        (prompt v2.0)

Paste this at the start of a scan session, with `<REPO>` replaced. It is the method;
[`0010_the-portfolio-audit.md`](0010_the-portfolio-audit.md) is the state.

---

Audit `<REPO>` and write down what you found. You do not repair it. The repair runs later,
from your row, in a session that never sees this repository's raw content.

Read `0010` §3 (method), §3.3 (your commands — four repositories cannot run the obvious
one), §3.4 (verdicts), and the `<REPO>` row in §4. If §6 records a correction binding v2.0
or later, §6 wins over this prompt.

## What this session may touch

| may | may not |
|---|---|
| read anything; run `pytest`, `pagespec`, `git`, read-only `gh` | modify any file in `<REPO>` |
| write its row in `0010`, commit and push the index audit branch | close or comment on an issue, edit a page, bump a pointer, rotate anything |

That boundary is why you may read an issue body, an extraction corpus or a scraped dataset
without special ceremony: nothing you read can reach anything that acts.

## Entry state — say so and stop if any of these holds

1. `git fetch --all` in the index and in `<REPO>`, then `python -m tools.entry_state --full`.
   `origin/main` is a stale local file; two passes on 2026-09-07 reached the same false
   conclusion from one.
2. **Index `HEAD` is not `origin/main`.** `entry_state` does not check this and passes
   without it — on 2026-09-10 it reported clean while `HEAD` was four commits and 470 lines
   ahead, in `tools/pagespec/clauses.py`, the module that computes axis C.
3. Anything uncommitted, or a pointer disagreeing with the index.

Record `git rev-parse HEAD` of the index and the gitlink you read — not "the main SHA". The
checker that answered is the one at that HEAD.

## The five axes

Order is load-bearing: secrets first because a finding there changes what may be written
down; code before docs because a doc claim is judged against code, never the reverse; page
last because it is the only axis a repair can break.

**Write your row after each axis.** An axis whose finding lives only in this session's
context is a finding that did not survive the session.

### E — secrets and confidential data

`0010` §2.3 already swept E1 across all thirteen repositories and found it clean, so unless
you have reason to re-run it, E here is **E0 and E2**.

**E0 — commit metadata.** `git log --all --format='%an <%ae>%n%cn <%ce>' | sort -u`. Blobs
are what `git grep` reads; authorship is not a blob. See `0010` R-1.

**E1, if you re-run it** — fetch what the remote will still serve first:
`git fetch origin '+refs/pull/*/head:refs/remotes/pr/*'`, then sweep
`git rev-list --all --remotes=pr`. GitHub keeps those refs indefinitely and this portfolio
squash-merges; 209 such commits across the twelve are invisible to `rev-list --all` alone.
Count hits before reading them, and do not pipe the sweep through `head`.

**E2 — personal and third-party data.** Take identifiers from `0010` §3.2's sources; if
`audit-identifiers.local` is absent, record `blocked` rather than sweeping for whatever you
happen to know. Then read the committed data artifacts and ask of each: whose data, under
what licence, does it name identifiable people or companies, and is it served publicly.
Check §3.3 before assuming `docs/` is published — it is for ten of twelve;
`wroclaw-air-insights` serves a workflow artifact and `token-budget` has no Pages site.

### A — code

Judge against `~/.claude/rules/good-practices.md`. Run the tests with §3.3's command —
`mini-traceroute` holds no Python and tests through CTest, so `pytest` there collects
nothing and exits 5, which is "no tests", not a failure. Paste real output; "tests look
fine" is not a result. Note guards that name something they cannot see: this portfolio has
shipped at least seven green over the defect they existed to catch.

Ten repositories carry `.codegraph/`; `doc-extract` and `pl-jobs-lora` do not.

### B — documentation

The question is whether it is still **true**, not whether it reads well. Bound the axis by
**artifact, not by file**: start from every figure, command, flag and path the docs claim,
and check whether something in the repository still produces it. `doc-extract` carries 86
markdown files and 9 321 lines, of which five hold 2 708 — the long tail is `results/*/` and
is checked by re-running a report, not by reading prose.

### C — the page

Run §3.3's command **before** judging any text, and record it. Then read the text as a
recruiter with sixty seconds: does the first screen say what this is and what it proved;
which sentences need two readings; which figures lack a unit, a baseline, or what they beat.
Propose shorter wording in the row — cut length, keep specificity; the recorded failure here
is descriptions that got short by going generic.

Do not edit the page. A repair session does that, against the clause the checker names.

### D — GitHub

`gh repo view` and `gh issue list --state open`. Read every open issue against the code and
say, with evidence, which of: already done · still real · obsolete · never was real. Sixteen
were open on 2026-09-10 across `ab-lab`, `apply-scout` and `mlops-car-price`; nine
repositories were clean. Also topics, homepage, stale branches, CI, `LICENSE`.

## Closing

1. Row complete in `0010` §4, including **what you did not check**.
2. Pattern rather than incident → §5.
3. Anything contradicting this prompt → §6, version `v2.0`.
4. Session brief to `.claude/sessions/<YYYY-MM-DD>.md`.
5. A repository with any `blocked` axis does not close — it returns to the queue.

A `clear` verdict produces no diff, so `code-reviewer` has nothing to review. Instead, name
in the row the single cheapest observation that would falsify each `clear` you wrote. A
verdict nobody can attack is a verdict nobody checked.

## Standing rules

- Figures come from an instrument, never a hand count. Three hand counts here produced 15,
  18 and 19 against a true 20; a fourth read 111 where counting commits rather than fields
  gives 113.
- Ask an instrument before quoting the record. `docs/` is several times the size of `tools/`
  and is where the stale figures live — including, until 2026-09-10, a reading of
  `doc-extract`'s attack corpus as having a 100 % success rate. That is the positive
  control; the real model scores 0.0 %.
- Stdlib, `git`, `gh`, `pytest`. Adding a dependency is out of scope for an audit.
- A guard that started failing is a finding, not an obstacle.
- Leave `GATE` in `tools/pagespec/__main__.py` alone; it is a ratchet with its own guards.
- If an axis was skipped, the row says so. An axis marked clean that was not checked is
  worse than one left open.
