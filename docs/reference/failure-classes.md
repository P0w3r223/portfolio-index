# Failure classes

Date: 2026-09-11
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`../adr/0009_the-ledger-is-addressed-not-partitioned.md`](../adr/0009_the-ledger-is-addressed-not-partitioned.md)
§3 step 3 (the decision that this exists),
[`../audit/0008_the-rollout-ledger.md`](../audit/0008_the-rollout-ledger.md) §3.7, §3.9 and
§3.10 (where these were defined, and where they stay)

**No document number, deliberately.** `ADR-0007` collides with `0007`, `ADR-0008` with `0008`,
and `ADR-0009` with `0009`; `ADR-0009` §0 records the third and refuses a fourth. This is a new
category with no series to join, so it takes a name. Cite a class by its **id**, never by a
section number of this file — that is the whole point of the ids.

---

## 1. What this is, and which direction it points

`0009` §6.2 row 5 called the taxonomy of defect shapes *"the most reusable asset this repository
has produced"* and *"unfindable"* — three sentences stating the whole method, near lines 435,
650 and 1 200 of one 3 400-line file. This is the findable form.

**It does not move the record.** Each class below is defined where it was defined, and this
file cites *into* `0008` rather than the other way. The dependency direction inverts on
purpose: a class gains occurrences as stages close, and a document that had to be edited every
time one recurred would be the ledger again under a new name.

**The ids follow `tools/spec.py`'s `c1.s6` pattern** — short, stable, and not a location. A
class id survives a renumber of `0008`; a citation of `0008` §3.9 does not, which is what
`tools/citations.py` now guards.

**Occurrence lists come from the instrument.** They were computed by matching the record's own
recurrence markers and mapping each hit to the section it sits in, not by reading for them —
the practice `CLAUDE.md` requires and the one three hand counts of clause 8's write sites
failed, producing fifteen, eighteen and nineteen against a true twenty. A list here is a
floor: the marker has to be written for the sweep to see it.

---

## SG — silent green

**A guard reports success over the defect it exists to catch.** The family this repository has
found in itself more than any other, and the reason its working rules say a guard is not proven
until a mutation reddens it. Every member shares one property: **the failure mode is
indistinguishable from the pass**, so no amount of running the suite reveals it.

### SG-1 — the guard is green under its own mutation

The guard runs, reads correctly, passes, and proves nothing, because the thing it asserts is
true for a reason other than the one it names.

*Defined:* `0008` §3.7 — two of twelve new guards, both written one commit earlier. One
asserted `"cycle" in detail` where the sentence it was meant to catch also ends in *cycle*; the
other's `seen` set was never entered, because the fixture's second hop lands back on the name
the walk started from.

*Recurs:* `0008` §4.15, §4.16, §4.18, §4.23, §4.25. **At least seven guards have shipped green
over the defect they existed to catch**, and every one was found by mutation and by nothing
else.

*The test:* break the thing the guard names; watch it go red **on that guard's own assertion**;
put it back. A non-zero exit is not red — `0010` §3.6 observation 2, where a skipped submodule
test reads as a pass.

### SG-2 — the guard cannot fail, because its tool excludes its subject

The assertion is correct, the tool answers a different question, and the answer is always the
one the assertion wants.

*Defined:* `0010` §3.6 observation 6. `tests/test_audit_identifiers.py` asserted that
`.gitignore` does **not** reach the committed template, using `git check-ignore` — which skips
paths already in the index, because tracked files are not subject to exclude rules. The
template is tracked, so the assertion answered *not ignored* whatever the pattern said.

*Recurs:* `tools/citations.py`'s own commit, from the other side. `git ls-files` excludes
untracked files, so while the module and its tests were unstaged the resolver could not see
itself and the suite was green; `git add` put them in the corpus and three of the module's own
sentences turned up as findings.

*The test:* ask what the tool excludes by default, then check whether the subject is in that
set. A mutation cannot reach this one — that is what makes it its own class.

### SG-3 — the branch with no guard at all

The rule has N shapes and the guard covers N−1. A mutation on the covered shapes is red, the
sweep over the corpus is clean, and the uncovered shape is invisible to both.

*Defined:* `0008` §3.9 and §3.10 — the role rule's four exception shapes, guarded on three,
three separate times, each pass declaring the previous instance closed. The fourth was the
focus ring, and **no page writes a `:focus` `border-color` in a house role**, so 97 of 97 was
true and the guard was still incomplete.

*Recurs:* `0008` §4.4, §4.9, §4.11, §4.15 carry the appearance counters — the record numbers
these up to the seventh.

*The test:* read the branches against each other rather than each against the corpus. **A
corpus sweep proves the rule against the corpus, and the corpus is not the rule** — `0008`
§3.10, and the single most reusable sentence in this record.

### SG-4 — the silent partition

A function whose contract is *these outputs partition the input* stops partitioning, and every
consumer downstream is wrong in a way that reads as ordinary data.

*Defined:* `0008` §3.10 — `split_schemes` when a dark query nests inside a dark query: inner
rules emitted twice, outer rules in both halves, the tail welding a closing brace onto the next
selector. Byte-identical to the code before the extraction, so the diff introduced no
regression; it introduced a **second consumer whose correctness depends on the split being a
partition.**

*Recurs:* `tools/citations.py`'s report, which computed `resolved` by subtracting the other
buckets — so a citation belonging to no named bucket joined the green column. Found by review,
2026-09-11, and repaired by counting `resolved` directly and asserting the partition in the
run.

*The test:* assert the partition itself, not a property of one part. Where the four parts must
sum to the whole, say so in an assertion.

---

## ST — a statement outliving its subject

**The record describes a state that has stopped existing.** Not a lie when written; the defect
is that nothing re-reads prose when the thing it describes moves. This family is why the
working rules say *record a correction rather than quietly fixing it*.

### ST-1 — the status cell that outlived the work

A plan's status column is what a reader scanning for the next task reads, and it is the last
thing a closing stage updates.

*Defined:* `0008` §3.11 — S13's cell read `in progress` for a day after the stage merged.

*Recurs:* §4.26 and §4.27 — S14's cell stayed `open` after both halves landed while saying
*"S14 is closed."* far into its own text. And `ADR-0009` itself read `proposed` while its own
step 1 was merging, 2026-09-11. `0008` §2.2, §3.7, §3.9, §4.5, §4.11, §4.16 carry the marker.

*The test:* a grep for open rows, run against the work rather than against the column.

### ST-2 — the sentence that outlived the partiality it described

Prose arguing from a fact keeps arguing after the fact moves.

*Defined:* `0008` §3.7, quoting `0007` §8.5 — **moving a fact into one cell does not sweep the
prose that argues from it.**

*Recurs:* `CLAUDE.md` said for a day that clause 8 and clause 4's `<title>` print and do not
gate, *"the open work, not an oversight"*, after S9 and S10 closed both. And its `docs/adr/`
line said *two numbers are now taken twice* until `ADR-0009` made it three.

*The test:* when a fact moves, grep for the fact, not for the section that held it.

### ST-3 — the correction applied in some places and left standing in another

A figure is corrected where the author was looking and survives where they were not.

*Defined:* `0008` §3.10 — the refuted *"seven of the nine"* corrected in two documents and left
standing in a test docstring, **three files apart from its own erratum**.

*Recurs:* `#122` corrected *"five of the eleven"* in `CLAUDE.md` and left two copies standing —
`0010` §6's row, the only section a scan session reaches unconditionally, and the `GATE`
comment block `CLAUDE.md` sends a stage editor to. Both repaired in `#125`, by **removing the
count** rather than correcting it: a figure in prose beside an instrument that computes it is
the defect, and correcting it only sets the next staleness date.

*The test:* grep the string, not the file.

### ST-4 — the premise that changed without a commit

Every other `ST` shape begins with work moving and prose failing to follow. This one begins with
nothing in the repository moving at all: a fact *about* the repository changes — its visibility,
its name, its owner — and every sentence arguing from that fact silently changes truth value.

*Defined:* [`0012`](../audit/0012_what-publication-invalidated.md) — `0011` §6 route A published
this index on 2026-09-17 without altering a byte of `main`, and six sites were arguing from *the
index is private*: a workflow comment still calling the decision open, `ADR-0004` §6's
counter-argument, `ADR-0009` §1's note on an unresolvable citation, `0007` §6 `c9.s2` —
**normative**, and pinned by literal in `tools/spec.py`, so the sentence and its pin have to move
in one commit — a `doc-extract` guard whose assertion stayed true while its stated reason did
not, and 21 lines across the twelve submodule `CLAUDE.md`.

*Recurs:* **on a second premise of the same event, and that is what makes it a class rather than
an incident.** Route A changed the index's *identity* as well as its visibility, and two artefacts
were written against the repository it stopped being: `0010`'s session queue, which named the
archive as the repository a session commits in, and `0011` §7's checklist, executed against a
repository it does not name and whose applied state survived only in a gitignored session brief.
Neither was predicted by the privacy half — a sweep for the word `private` returns neither.

*The test:* **sweep for the premise, not for the fact.** The fact lives in the settings and has
no occurrences in the tree; the premise is a word — here `private` — and the corpus is every
tracked file *outside* the dated record. Both halves are claims: `0012` F-10 sat inside a declared
scope and the run still came back one file short, and nothing an instrument prints distinguishes
that from a clean sweep.

---

## FG — a figure with no instrument

**A number that no committed code produces.** `CLAUDE.md`'s rule — *figures come from an
instrument, not from a hand count* — is the standing answer, and these are the shapes it was
written against.

### FG-1 — the number nobody re-derived because it looked derived

An arithmetic result carried forward through a change that invalidates one of its terms.

*Defined:* `0008` §3.7, naming `0007` §8.4. The clause 1 census was written as *124
declarations, 108 naming the house role* — 124 minus sixteen exceptions, without excluding the
eleven `color-mix()` declarations the clause does not reach. **The subtraction was the whole
error.**

*Recurs:* `0008` §4.11, §4.13, §4.15, §4.17, §4.23, §4.24, §4.29. Three hand counts of clause
8's write sites produced fifteen, eighteen and nineteen against a true twenty; a count of the
citation graph read 81 across 22 files because ten of them were gitignored session briefs; and
on 2026-09-11 that same graph was miscounted twice in one day by two independent careful
readings — once by conflating *no document number* with *another document's number*, once by
matching against a path — which is the measurement `ADR-0009` §1 turns into its argument.

*The test:* compute it, print it on every run, and do not write it down. `0008` §4.11 records
what a hand-typed figure costs in exactly the lines that then went stale again.

### FG-2 — the figure taken from a document instead of from the instrument

A number is read out of the record, which read it out of an earlier record.

*Defined:* `0010` §1. A self-review cited a **100 % attack success rate** in `doc-extract` as a
property of the corpus. That is `gullible`, the positive control, 100 % by construction; the
real model scores 0.0 %.

*The test:* ask the instrument that produced the figure, not the document that quotes it.

---

## SC — scope discovered during the work

### SC-1 — the row whose central assumption is false

A planned item is costed from a description, and the description is wrong about what is there.

*Defined:* `0008` §4.7, and it is the precedent the record now counts: **§4.20, §4.23, §4.25,
§4.28, §4.29, §3.11 and §2.2 all invoke it**, up to the seventh time. S7's row named four items
and the stage touched nine repositories. S8a's row implied eight READMEs and the scope was
twenty-six sites across all twelve. S14's row assumed a regression guard over a clean corpus,
and nine form-control boundaries were failing SC 1.4.11 at 1.17:1.

*Recurs, and twice the row turned out not to exist at all:* `0008` §4.29 — the seventeen called
page work are a partition error in three shapes, and zero of them is a page defect. And
`ADR-0009` §1 — two of `0009` §7 row 9's three destinations do not exist.

*The test:* **re-derive the scope before the stage rather than during it.** The figure then
moves on paper instead of on the day, which is the only reason any of these were cheap.

---

## 2. How to add a class

A class enters when a shape has occurred **twice** and the second occurrence was not predicted
by the first. One occurrence is an incident and belongs in `0008` §4.x, where it happened.

Give it an id in an existing family or open a new two-letter one, state where it was defined,
list where it recurred, and — the part that earns the entry — **state the test**: what a reader
does differently to catch the next one. A class with no test is a story.

Do not move the record to write one. The occurrences stay where they are; this file cites them.
