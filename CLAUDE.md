# CLAUDE.md — portfolio-index

Guidance for Claude Code (and any contributor) working in the portfolio index.

## What this repository is

The **private** index of a twelve-repository portfolio. It is not a package: nothing here is
installed, imported by a sibling, or published — `pyproject.toml` exists so `pytest` finds the
checker, and says so in its first line.

**That first word is wrong here, and deliberately left standing one line above.** `0011` §6 step 0
took route A on 2026-09-17: this repository is the *published clone*, and the private index it was
cloned from is the one the sentence above describes. The line is kept because every `docs/audit/`
document reasons from it, and rewriting one sentence while eleven documents still assume it is how
a record starts lying in two directions at once. **Read `private` as naming the origin, not this
copy** — and the same applies to "The public landing surface" argument below, which is about the
profile README being the recruiter's entry point and survives the move unchanged.

Two things live here and nowhere else, and they are the reason a session starts here at all:

- **The page specification.** `docs/audit/0007_divergence-and-the-page-spec.md` §5 is normative
  prose — eight clauses plus §6's clause 9 and §5.0's governing rule. The twelve published pages
  are held to it.
- **The instrument that enforces part of it.** `tools/pagespec` reads eleven committed surfaces
  from the submodule working trees and one from its live URL, prints a conformance table, and
  since `0008` S-gate **refuses** when a clause in `GATED` fails.

**The public landing surface is not this repository's `README.md`.** *This paragraph used to
argue from privacy — a recruiter could not open the index, so the profile was the only surface.
Both are public since 2026-09-17 and that reason is gone. The conclusion is not:*
`github.com/P0w3r223` is the address that gets handed out, and this repository is reached
**from** it — since 2026-09-17 by an explicit link in the profile's closing section, which also
points the profile's "measured rather than asserted" claim at the place it can be checked.
The profile README is a separate repository (`P0w3r223/P0w3r223`) and is still **carried by
nothing here** — no clause, no test, no row of `SURFACES` — which `0009` §7 row 11 has held open
since before the move and which the move made more expensive, not less: the profile now sends
readers here, and an edit to it is still one nothing checks. `README.md` in this repository is
an index written in a recruiter's register. Do not repair one and assume the other moved.

## Architecture

```
tools/pagespec/       the checker — standard library only
  sources.py            the surface registry and the ONLY I/O; everything else is pure
  render.py             HTML -> Page (title, headline, tables and text nodes with ancestry),
                          and the element stream S13 added: every element in document order
                          with its attributes, its parent, and a bounded ancestor walk
  css.py                CSS -> rules, with comments stripped and media conditions flattened
  colour.py             WCAG arithmetic; all three of contrast(), resolve() and composite()
                          are called since S13 — the line here said the last two ship unused
                          until 2026-09-09, and tools/spec.py c1.s6 said it in the same words
  clauses.py            clauses 1-8 as pure checks over one Loaded
  selector.py           which elements a rule reaches, and the shapes it refuses to answer for
  geometry.py           whether one shape covers another, from the coordinates the markup
                          already writes — not ADR-0004 §4's deferred geometry, which needs a
                          rendered box; ADR-0008 §3 is the distinction and it is load-bearing
  paint.py              what colour an element is painted, and at what alpha — every
                          candidate, not the winner
  contrast.py           every usage site, its implied threshold, what it is painted on,
                          and — since S14b — the verdict over two of its three keys. The
                          third, `contrast ground`, cannot take one: it reports what the
                          checker could not read, and no page is more conformant for
                          being legible to it. *This line said the module has no PASS
                          and no FAIL branch and that a guard read it statically to
                          stop S14 adding one silently. It did, it was, and that is
                          exactly what happened — loudly, which was the design*
  __main__.py           the report, two censuses, and the GATE ratchet with its three states
tools/spec.py         every normative sentence of 0007 §5-§6, and what carries it
tools/citations.py    every §N reference in the index, and whether the section it names
                        exists. Four states; only `unresolved` gates, via tests/. ADR-0009
                        §3 step 1 — the answer to nothing in `tools/` reading 0008 at all
tools/entry_state.py  0008 §6's two repository-state rows, at two depths
tests/                the guards; fixtures/ are reductions of record, see its README
docs/reference/       failure-classes.md — the defect shapes this project keeps finding in
                        itself, with an id each and the test that catches the next one.
                        **No document number**, and ADR-0009 §0 is why: three are taken
                        twice already. Cite a class by its id; the file cites *into* 0008
                        rather than moving it
docs/adr/             what carries what; 0004 is the load-bearing one, 0005 the clause
                        registry, 0006 the gate registry and the twelfth surface, 0007 S8a's
                        design, 0008 the ground of a usage site and why S13 is a census
                        before it is a verdict, 0009 why the ledger is addressed rather than
                        partitioned, **0010 the authorship test** — a clause may be asked of
                        a surface only where the portfolio writes the bytes that decide the
                        verdict, and the criterion has an instrument: a verdict that moved
                        with no commit in the portfolio belongs to the host. It answers
                        `0012` F-1, `0009` §7 row 11 and `0012` F-8 at once.
                        **An ADR number is not an audit number**, and
                        **numbers are taken twice, and no count stands here**: `ADR-0007`
                        is the text layers against bare `0007` the page spec, `ADR-0008`
                        the contrast ground against bare `0008` the rollout ledger,
                        `ADR-0009` the ledger decision against bare `0009` the whole-system
                        review, and `ADR-0010` the authorship test against bare `0010` the
                        portfolio audit. The last two arrived deliberately, each with its
                        reasoning and its refused alternative, in that ADR's own §0.
                        **A bare number in this repository means the audit document.**
                        *This line carried a figure and it was wrong twice — **two** until
                        2026-09-11, **three** until 2026-09-17. The figure is removed
                        rather than corrected a third time, which is `ST-3`'s own remedy
                        and the fix `#125` used on two other counts: a number in prose
                        beside a directory that answers it only sets the next staleness
                        date. Count `docs/adr/` against the audit series if you need one*
docs/audit/           the record: 0001-0006 earlier sessions, 0007 the spec, 0008 the plan,
                        0009 the whole-system review and what the passes since got wrong,
                        **0010 the portfolio audit — the plan work is taken from now**, with
                        its two prompts beside it: `0010_scan-prompt.md` reads and may not
                        act, `0010_repair-prompt.md` acts and may not read a repository's raw
                        data. **`0008` has one open row and it is not work**: S8c is a refusal
                        on measurement — available, unscheduled, costed as its own project —
                        so a session asking *what next* reads `0010` §3.1 and §4, not
                        `0008` §3. **0011 the pre-publication security audit** — what became
                        readable when this repository stopped being private, the route A that
                        produced it, and §10 on the six defects found in the audit itself.
                        Its §9 states three redaction rules and §3.3 three false positives;
                        **run its grep before extending it**, because all three rules have
                        been broken four times between them and never by carelessness.
                        **0012 what publication invalidated** — the sentences route A stopped
                        being true without touching a byte, which is why no test caught them.
                        `0012` §2 is why this repository has no instrument for that class;
                        `0012` §4 is the findings, of which **F-1 is open and normative**:
                        `0007` §6 `c9.s2` argues from the private index, `tools/spec.py` pins
                        it by literal, so the sentence and its pin move in one commit — and it
                        is the same question as `0009` §7 row 11. `0012` §5 is the applied
                        state of `0011` §7 read from the API, `0012` §6 is what to do with
                        work stranded in the archive, and `0012` §7 names the premise the
                        sweep did not cover — **this line ranks nothing on purpose**, because
                        a map is read as current and a ranking outlives the row it ranks
.github/workflows/    pagespec.yml — core (no submodules), surfaces (gates), live (scheduled).
                        Its two `paths:` filters are tied to `sources.SURFACES` by a `core`
                        test, and also name `.gitignore`. **That last entry now guards
                        nothing**: it was there for `tests/test_audit_identifiers.py`, retired
                        2026-09-11 with the identifier sweep, and it is kept because a
                        `.gitignore` change can move what the checker reads. No test reads
                        the file today — `test_report.py` and `test_sources.py` only cite it
<twelve directories>  the submodules; each is a standalone repository with its own CLAUDE.md
```

**Which document is which**, because they are not interchangeable and `ADR-0004` §5 is the rule
that separates them: `0007` §5 keeps the **rules**, the checker owns the **conformance table**,
and `0008` owns the **plan and its status**. A measurement written into a normative document
cannot be accepted without being frozen — `0007` §3 was corrected five times before that split.

## Commands

```bash
python -m tools.entry_state              # the entry state, quick
python tools/entry_state.py --hook       # verbatim what the session-start hook runs. By path,
                                         #   because the module form needs the root on sys.path
                                         #   and so depends on the hook's working directory;
                                         #   `--hook` is what keeps a real finding from reading
                                         #   as a broken hook
python -m tools.entry_state --full       # every pointer against its own remote, before a stage

python -m tools.citations                # every §N reference, and the heading it resolves to.
                                         #   Prints and exits 0; the guards refuse a citation
                                         #   naming a section its document does not hold

python -m tools.spec                     # every normative sentence, and what carries it.
                                         #   Prints and exits 0 — the uncarried rows are the
                                         #   point, and no instrument can tell an open item
                                         #   from a decision

python -m tools.pagespec                 # the conformance table; exits 1 if a GATED clause fails
python -m tools.pagespec --detail        # every finding, which is what CI runs
python -m tools.pagespec --report-only   # print and exit zero whatever it finds
python -m tools.pagespec --only ab-lab   # one surface
python -m tools.pagespec --fetch         # include wroclaw, which commits no HTML

python -m pytest                         # the whole suite
python -m pytest -m 'not submodules'     # what CI's `core` job runs — no sibling on disk
python -m pytest -m submodules           # only the tests that read a working tree
python -m pytest -m submodules --fetch   # what the scheduled `live` job runs: the same
                                         #   guards over the twelve the gate covers, not
                                         #   the eleven that commit a file. Reads the wire
```

## Working rules

- Branches and pull requests, [Conventional Commits](https://www.conventionalcommits.org/),
  and a description that says **why**. One stage per pull request where the stage allows it.
- **Every stage closes with a `code-reviewer` pass** before it is proposed as merged work.
- **A guard is not proven until a mutation reddens it.** Break the thing the test names, watch
  it go red, put it back. `0008` records at least seven guards that shipped green over the
  defect they existed to catch, and every one was found this way and no other.
- **Figures come from an instrument, not from a hand count.** Clause 1's census and the role
  census are computed on every run for this reason; three hand-counts of clause 8's write sites
  produced fifteen, eighteen and nineteen against a true twenty.
- **Record a correction rather than quietly fixing it.** A reader carrying the old figure
  forward is how `0006` §2.4 happened. The errata sections of `0008` are the form.

## What not to do

- **Do not hand-edit `GATE`** (`tools/pagespec/__main__.py`) as part of unrelated work. It is a
  ratchet: each row names a finding prefix, what the gate does with it, and — for anything the
  gate does not refuse on — why. Widening it past the measurement is caught by
  `test_the_ratchet_holds_no_clause_the_committed_surfaces_report_failing`, and **narrowing it
  now has two shapes with two guards, in two different jobs.** *Deleting* a row is caught by
  `test_the_ratchet_cannot_be_narrowed_either_every_clean_clause_is_gated` — but only in the
  `surfaces` and `live` jobs, because it reads the sibling working trees, so a pull request
  green on `core` alone proves nothing: dropping every row but `1 `, which un-gates seven
  clauses at once, still passes `pytest -m 'not submodules'`. *Demoting* a row to
  `report-only` un-gates it just as completely and **no corpus can see it**, because a
  report-only row is an explanation — so that one is caught by
  `test_the_report_only_set_is_pinned_because_it_is_policy_and_not_a_measurement`, in `core`,
  and adding a row there means editing that pin too. The second shape arrived with the
  registry and shipped green for one commit; `ADR-0005` §4 had predicted it for a derivation
  nobody had taken yet.
  *This paragraph said narrowing was caught by nothing at all, which stopped being true at
  `#83` and was found by the audit of 2026-09-07 — a reader who believed it would not trust the
  guard that would have stopped them.* Clause 8 and clause 4-`<title>` entered with S9 and S10
  on 2026-09-08, so the registry covers every clause the spec carries **today**, and
  `0009` §7 row 12's contrast clause **entered with S14b on 2026-09-10**: `contrast text` is
  gated, `contrast marks` is report-only, and `0007` §5 clause 1 carries the obligation
  sentence as `c1.s6b`.
- **The eleven/twelve trap is now the instrument's, not yours — and the price is that a new
  clause enters in two steps rather than one.** `wroclaw` commits no HTML and republishes from
  a Pages artifact rebuilt daily, so its page does not move when its pull request merges, while
  the floor guard reads the eleven at the pinned gitlinks. Until `0009` §7 row 13b that guard
  **demanded** the widening the moment those eleven went clean, so a pointer bump armed it while
  the twelfth still failed and the morning's `live` run went red on a merge that was green —
  S9 and S10 both navigated that by hand. Since row 13b the sweep takes its mode as a parameter:
  `surfaces` reads the eleven, the scheduled `live` job reads the twelve with `--fetch`, and
  the registry has a `pending` state for exactly this gap. So: land the siblings, bump the
  pointers, add the key as `Ratchet(prefix, PENDING_STATE, reason)` — the fetchless floor
  accepts that and the ceiling still refuses a regression — then let the next `live` run
  **demand** its promotion to `GATED_STATE`, or leave it pending if the twelfth still fails.
  Confirming by hand with `python -m tools.pagespec --fetch` or a `live` dispatch still works
  and is faster; what changed is that forgetting to is no longer silent. `0008` §4.15 records
  when the trap bit, and §4.18 what closing it cost.
- **Do not weaken a guard to make it pass.** A guard that has started failing is a finding.
- **Do not add a dependency.** The checker is standard library only and `pytest` is the sole
  test dependency; the `core` CI job installs nothing else.
- **Do not commit a page from here.** The pages belong to their own repositories and are
  generated there; most carry a page test of their own. No count is given, because three
  different sweeps for one produced three different answers — ask the trees, and mind that a
  repository can guard its page without the string `docs/index.html` appearing in its tests.
  What is settled: **`mini-traceroute` holds no Python at all** — no `pyproject.toml`, zero
  `.py` files — so it can carry no local page test, which makes it the one surface the index
  checker guards alone. This repository re-points submodules; it does not edit them.
- **Do not ask the owner for personal identifiers, and do not reintroduce a sweep that needs
  them.** The audit's identifier half was **retired on 2026-09-11 on the owner's decision** —
  the template, its six guards and `0010` §3.2's sources table are gone, and `0010` §6 records
  it. The axis it belonged to survives as third-party data only, which costs the owner nothing.
  A session that finds this inconvenient should read `0010` §3.2 before proposing to rebuild
  it: the sweep needed the owner's private values as search literals, and running it meant
  those values entering a session transcript — which the design's *never committed, only
  counted* protection does not reach.

## The published surfaces, and what the gate does not say

Twelve surfaces. Eleven commit a file; `wroclaw-air-insights` commits no HTML at all and exists
only at its URL. `reports/site/` in that repository is a gitignored local build and reading it
has produced a wrong answer that survived a session.

**`--fetch` is not "and also wroclaw".** Since `#90` it judges *every* surface on the bytes it
actually serves and additionally compares those against the eleven committed files under the
`served` key — `0009` §3.1's C1. Only the scheduled `live` job passes it, and a test refuses the
flag in any job a push or a pull request reaches. So `surfaces` answers from the pinned gitlinks
and `live` answers from each sibling's published page, and **the two can disagree**: that is the
point of the flag and not a defect. A wire failure is `undecided` and refuses nothing; a page
answering 4xx, and a surface whose committed file has gone missing while the wire answers in its
place, both refuse.

The gate is **deliberately partial**. `UNDECIDED` never gates, which is what lets the checker be
honest about `color-mix()`, an unread media condition, and a headline it cannot judge.
`python -m tools.pagespec` exiting 0 therefore means *no gated clause failed*, and not *every
clause passes*. What else stays outside the gate is now printed by the run itself, under
`gate policy`, with the reason beside it — `served` and, since S14b, `contrast marks`.
**That second row is the first one whose key actually fails**: four of the eleven surfaces
report it, so a run now prints `FAIL` and exits 0, and the only place saying why is that
block. *The sentence above said `served` was the only row there, and stayed true for two
days.*

*This paragraph said until 2026-09-08 that clause 8 and clause 4's `<title>` half print and do
not gate, "the open work, not an oversight". S9 and S10 closed both the day before, and the
sentence describing the partiality outlived the partiality it described. Found while closing
`0009` §7 row 13b, by a reader who came for the paragraph below it — which is the argument for
printing the policy rather than writing it down.*

Half the specification cannot be carried from here at all, by construction: a repository's own
artifacts, and `0007` §5.0's rule that every figure a surface prints is a figure a committed
artifact prints. Those are the submodules' own page tests. `ADR-0004` is the decision and its
amendments record how the split moved.

## Code intelligence

**There is no `.codegraph/` here.** Ten of the twelve submodules carry one and their `CLAUDE.md`
say so; `doc-extract` and `pl-jobs-lora` carry neither the index nor a mention of it. This
repository has none either, so the `codegraph_explore` MCP tool and the `codegraph` CLI answer
about whichever project you point them at and about nothing in `tools/` or `docs/`.

Grep, Glob and Read are the tools here, and the Python is small enough that this costs nothing.
**The record is the large thing** — `docs/` is several times the size of `tools/`, and `0008`
alone is longer than any module in it — so prefer reading a named section over reading a file,
and prefer the checker's own output over any figure the record quotes. No line count is written
down here on purpose: a figure in this file would be a hand-typed one, which is the practice the
section above forbids.

## Read the entry state before quoting anything

`0008` §6 is a table of assumptions to verify **before each stage, not once**. Two of its rows
are now `python -m tools.entry_state`; the rest are still yours to check, and the module's
docstring names which.

- **`git fetch` first.** `origin/main` is a local file a session inherits and nothing refreshes
  on its own. On 2026-09-07, an hour after `#77` merged, two passes independently reported the
  index as unmerged with no pull request open — which is exactly what a stale ref plus a
  *closed* (not never-opened) pull request looks like. Three signals agreed with the false
  hypothesis at once.
- **This repository squash-merges.** A branch commit is never reachable from `main` and never
  will be. Cite the commit on `main`; a cell citing the branch SHA is citing a commit that does
  not exist for any reader. `0008` §4.12 records the S-gate row doing it.
- **Check the working tree before quoting the checker.** A submodule on a fix branch, or a
  round of uncommitted edits, means `python -m tools.pagespec` is reading pages nobody has
  published. That has happened, for an hour, across twelve `CLAUDE.md` and eight `README.md`.

*This section sits last on purpose.* It is the one part of this file that has already been
paid for: two passes reached the same false conclusion on 2026-09-07 because none of it was
loaded, and a reader's attention is weakest in the middle of a document and strongest at its
end. Everything above tells you what this repository is; this tells you what to check before
you say anything about it.
