# The ledger is addressed, not partitioned

Date: 2026-09-11
Status: accepted — the owner chose this option over the three alternatives on 2026-09-11,
and steps 1 and 2 landed the same day (`#126`, `#127`, and the move of `0008` §4.11's
policies into `ADR-0006` §7). Steps 3 and 4 remain. *This read `proposed` while its own
step 1 was merging, which is `0008` §3's status column doing the thing that section
records against itself twice.*
Author: Piotr Cząstkiewicz + Claude
Related to: [`../audit/0009_the-review-of-the-whole-system.md`](../audit/0009_the-review-of-the-whole-system.md)
§7 row 9 (the row this answers),
[`0004_what-carries-the-page-spec.md`](0004_what-carries-the-page-spec.md) §5 (the
three-lifetime rule this applies),
[`0006_the-gate-registry-and-the-twelfth-surface.md`](0006_the-gate-registry-and-the-twelfth-surface.md)
(the home §4.11's policies move to),
[`../audit/0008_the-rollout-ledger.md`](../audit/0008_the-rollout-ledger.md) (the subject)

Cite this as `ADR-0009`. Bare `0009` means the whole-system review in `docs/audit/`.

---

## 0. The number, because it is the third collision and not the first

This is `ADR-0009` and `docs/audit/0009` is the review it answers. **Two numbers were
already taken twice** — `ADR-0007` against `0007`, `ADR-0008` against `0008` — and `CLAUDE.md`
governs them with one rule: *a bare number in this repository means the audit document*.

The alternative considered and refused was skipping to a free number. It relocates the
collision rather than ending it: `docs/audit/`'s next document is `0011`, so an `ADR-0011`
collides on the day that one is written, and `docs/adr/`'s filing convention is `nnnn_slug.md`
for every one of its eight existing entries. What makes this instance worse than the two
before it is only that the subject is `0009` §7 row 9, so *"ADR-0009 answers 0009 row 9"* is a
sentence a reader has to parse twice.

**So the rule is restated rather than bent: cite this document as `ADR-0009`, never bare.**

**The rule does not extend to a bare section reference, and §3 step 3 is not this section
contradicting itself.** `CLAUDE.md` governs bare *document* numbers; a bare `§4.x` resolves to
nothing by convention, and §1 measures 59 such lines across 19 files — 27 inside a document
that owns a `§4.x` subsection of its own, so the reference may be a self-citation, and 19 in
`tools/`, `tests/` and a fixture, where it cannot be. That is step 1's subject. And the reasoning above binds only a document
that must take a number in an existing numbered series: `docs/reference/` is a new category
with no series to join, so the failure classes take a name instead — the collision evidence
here is exactly why.

## 1. Context

Every figure below was measured at `f66b13c` on 2026-09-11, with the command beside it, and
frozen here by `ADR-0004` §5. Each was taken with `git grep` / `git ls-files` — the filesystem
holds gitignored content no clone has, which is how an earlier count of this same row read 81
across 22 files with ten of them in `.claude/sessions/`.

`wc -l` on the tracked file: **3413 lines**. `grep -nE "^## [0-9]"` puts the section
boundaries at 14, 29, 102, 586, 3389, 3402, so **§4 is 2803 lines — 82.1 %** — and §3, which
holds the stage table every session reads, is 484.

`git grep -nE '§4\.[0-9]' -- . ':!docs/audit/0008_the-rollout-ledger.md'` returns **162 lines
in 28 tracked files** — this document excluded, since it cites `§4.x` nine times itself. Three
disjoint buckets over one key, summing to 162 exactly. **Each is measured against the line's
content, with `git grep -n`'s `path:line:` prefix stripped first** — see the erratum below:

| bucket | lines | command |
|---|---:|---|
| content carries `0008` | **89** | `… \| sed 's/^[^:]*:[0-9]*://' \| grep -c '0008'` |
| content carries no document number | **59** | `… \| grep -vcE '000[1-9]\|0010'` |
| content names another document, not `0008` | **14** | `… \| grep -E '000[1-9]\|0010' \| grep -vc '0008'` |

**The `0008` key under-collects and does not over-collect, which is the useful half of this.**
`ADR-0008` appears in the content of exactly **two** of the 162 lines, and both also carry a
genuine bare-`0008` citation of the ledger — so a sweep keyed on `0008` gathers no false
positive at all. It cannot: `docs/adr/0008_the-ground-of-a-usage-site.md` has **no `§4.N`
subsections**, its `## 4.` running from line 83 to 104 with no `###` inside, so no `§4.x`
citation can resolve to it. **The set is therefore bounded below at 89, and the unbounded part
is the 59-line residue alone** — every one of which needs a read, because a bare `§4.x` may be
a self-citation.

> **Erratum, taken before this document was proposed rather than after.** The three buckets
> above first read 70 / 21 / 20 and were wrong, all three, in one way: the greps ran over
> `git grep -n`'s output *including the path*, so `0008` in the path
> `docs/adr/0008_…md` counted as a citation of that document and the no-number bucket dropped
> every line whose **filename** held a digit run. The first version of this section then built
> two claims on the bad figures — that neither grep direction bounds the set, and that an
> earlier architecture pass had "folded `ADR-0008` into `0008` and reported 87". **Both are
> withdrawn.** `89 − 2 = 87` is the correctly disambiguated count, so that pass's figure was
> right and the accusation was the miscount. Found by the review of this commit, which
> re-measured against content. *The general argument for step 1 is unharmed and is now carried
> by this erratum instead: the citation graph was miscounted twice in one day, by two
> independent careful readings, in a repository whose rule is that a figure comes from an
> instrument. There is no instrument here to come from.*

Concentration is extreme where it costs most. `git grep -nE '§4\.11'` outside the ledger:
**43 lines in 14 files**, and `tools/pagespec/__main__.py` alone carries **10** of them.

**Two of the row's three destinations do not exist.** The failure-class taxonomy is defined in
**§3.7, §3.9 and §3.10** — §4 holds its recurrences, not its definitions (*"the fifth
appearance"*, §4.4; *"the sixth and seventh"*, §4.9) — so it cannot be lifted out of §4 while
the same row keeps §3 in the ledger. And the report prints *today's* census; §4 records a
history of censuses — 153 → 88 → 26 — for which a live report has no slot and `CLAUDE.md`
forbids a retype.

**The fact that decides the shape: nothing reads `0008`.** `tools/spec.py:556` sets
`SPEC` to `0007` and is the only module in `tools/` that opens a record document at all. Every
citation of `0008` is prose in a comment or a docstring. A partition therefore breaks
**silently**, and there is no guard to redden before the move — which is this repository's own
worst failure class, the one `0008` §3.7, §3.9 and §3.10 name and which `0008` records at least
seven times against itself.

### 1.1 What the submodules cite, because the row's evidence is wrong

`0009` §7 row 9 keeps this an index-only stage on the grounds that the submodules *"cite `0008`
§3.6 and nothing else (`apply-scout` 3, `auth-log-scan` 2)"*. Measured with `git grep` in all
twelve working trees:

| repo | what it actually cites |
|---|---|
| `apply-scout/tests/test_docs_page.py` | §3.6 **×4** — `:914`, `:963`, `:1040`, `:1075`, the last without backticks — plus a bare `` `0008` `` at `:1028` |
| `apply-scout/tests/expected/docs_page_tokens.md:5` | the same bare string, **in an asserted golden file**, so it lives in two places at once |
| `auth-log-scan/tests/test_site.py:197, :231` | **§3.9 and §3.10**, twice each — **not §3.6 at all** |
| `wroclaw-air-insights/.github/workflows/refresh.yml:23` | `0008` **S6** — a stage id, in a submodule's CI workflow |
| `ab-lab/sitegen/theme.py:18, :21` | `0008` **S7** ×2 — in the production code that generates a page |

**Eleven sites in five files across four repositories, not five in two**, and the row is wrong
about the section, the count and the list. **The conclusion survives**: `git grep -nE
'§4\.[0-9]'` across all twelve returns exactly one hit, `pl-jobs-lora/docs/index.html:83`, and
it cites `0007` §4.1 rather than `0008`. No submodule reaches §4, so this stays index-only — on
a measurement rather than on the sentence that claimed it.

*That single hit is worth its own line: a **published public page** carries a section number of
a document in a private repository. A reader of that page cannot resolve it, and renumbering
`0007` would falsify it silently. It is out of this decision's scope and recorded so the next
reader does not have to find it twice.*

## 2. Options considered

### A — freeze, reorder, renumber nothing

Sort §3's and §4's subsections numerically (§3 runs 3.1, 3.2, 3.5, 3.3, 3.4, 3.11, 3.6, 3.7,
3.9, 3.10, 3.8) and move **§6** ahead of §4 — §3 already is, beginning at line 102 against
§4's 586. **No identifier changes and no citation breaks** — all 162 external lines stay valid
without an edit. Effort S, risk low. Delivers navigability and nothing else.

### B — the row as written: ledger / taxonomy / measurements

Effort L, risk high. Requires re-pointing the set §1 shows is unbounded by any grep, with no
instrument; contradicts itself on §3, where the taxonomy is defined; and its third destination
is empty for every historical census.

### C — one file per stage under `docs/audit/0008/`

Effort L, risk high. Serves §3 and §6 perfectly, destroys every `§4.x` identifier including the
43 lines §1 measures, and scatters the taxonomy further — worsening the one thing row 9 exists
to fix.

### D — address the ledger instead of partitioning it

Build the citation resolver first, promote the two concepts the code actually cites to
first-class homes, leave every section number where it is, migrate opportunistically.
Effort S + S + M, risk low, **zero citations broken**.

## 3. Decision

**Take D, with A's reordering as a separable pull request.**

1. **A `core` guard resolves every `§N.M` citation of `0008` in tracked index files** against
   `0008`'s own headings, on `tools/spec.py`'s heading-boundary pattern — the slice fails by
   naming the heading it could not find, which `tests/test_spec.py` already proves. **`docs/**`
   is added to both `paths:` filters in `.github/workflows/pagespec.yml`**, on the precedent set
   in that same file for `.gitignore`: a guard reading a file whose path is not in the filter
   runs in **no job**. *That precedent was set by two entries; the second, the audit's
   identifier template, was deleted with its guards on 2026-09-11 and the precedent stands on
   the one that remains.* The guard resolves the 89 sites
   whose content names the ledger; **the 59 carrying no document number are not an edge case
   but a read-and-annotate backlog** — 36 % of the graph, 19 of them in `tools/`, `tests/` and
   a fixture where a self-citation is impossible, so those are resolvable first and cheaply.
   The exemption list is emitted by the guard on every run rather than typed, so it shrinks
   visibly as the backlog is worked.
2. **§4.11's three gate policies are promoted to `ADR-0006`.** They are decisions, cited ten
   times by `tools/pagespec/__main__.py` as the reason `GATE` behaves as it does. `ADR-0004`
   §5 states a *lifetime* split and the freezing rule rather than this in so many words;
   **reading it as "a decision belongs in a decision document" is an extension of it, and is
   stated here as one.** §4.11 keeps its number and gains one sentence naming the normative
   home.
3. **The failure classes get `docs/reference/failure-classes.md`** with **named** ids on
   `tools/spec.py`'s `c1.s6` pattern, and **no document number** — §0 is why. Each class carries
   its occurrence list as citations *into* `0008`; the dependency direction inverts.
4. **No section is renumbered, no section is deleted, no citation is re-pointed in a sweep.**
   The code-side citations move to class names when their file is next touched for another
   reason.

**The argument that tips it** is row 9's own strongest sentence: *the mechanical half is not
mechanical*. That is a statement about a missing instrument, and this repository's answer to a
missing instrument is never to do the work more carefully — it is to build the instrument and
let it demand the work. §1's erratum is that argument arriving as evidence, and it is worth
more than the claim it replaced: **this citation graph was counted by hand twice in one day, by
two independent careful readings, and both were wrong** — the first conflating "no document
number" with "another document's number", the second matching against a path. Neither was
careless. There is simply nothing to check a count against.

## 4. Consequences

- **`0008` stays 3413 lines.** Stated as the price rather than buried: the growth argument
  expired when S14b closed and no stage is open, so length is not the live risk. The 43 lines
  pointing from `tools/` and CI into narrative are.
- **A new guard runs in `core`, and `docs/**` enters the `paths:` filter** — so `docs/`-only
  commits stop being CI-invisible. `0008` §3's Sx cell records `b416c83` having no run at all
  for exactly this reason, and reads it as the filter working; it is also the filter hiding
  every future docs guard.
- **And it arms `surfaces` as well, which is the cost half of the same bullet.** `paths:` is
  per *trigger*, not per job, and only `live` carries an `if:` (`pagespec.yml:122`). So every
  docs-only push and pull request will also check out the submodules and run
  `pytest -m submodules` with the gate live — a sibling page regression at the pinned gitlinks
  then blocks a documentation merge. There is no `paths:` shape reaching `core` alone; a
  job-level `if:` on `surfaces` is the lever if that trade is refused, and it is left to the
  plan rather than decided here. *Verified in the filter's favour: adding `docs/**` reddens
  neither `test_the_workflow_triggers_on_every_repository_the_registry_publishes` — its
  `_A_REPOSITORY` pattern at `tests/test_sources.py:214` drops any entry with a separator. The
  second guard checked here, `tests/test_audit_identifiers.py`, was deleted on 2026-09-11 with
  the identifier sweep, so no test reads either filter's literal contents today.*
- **Neither the conformance table nor the gate can move.** Nothing reads `0008` and no `GATE`
  row is touched. Proof is byte-identical checker output plus a mutation on the new guard,
  under `0010` §3.6's six observations.
- **What is given up is a short ledger.** B and C stay available and become *cheaper* after
  this, not dearer: once the resolver exists, a renumber is mechanical for real, because an
  instrument finds the sites and verifies the result. In the other order it never is.
- **Revisit when** the resolver reports that a majority of the code-side citations have
  migrated to class ids, or when `0008` gains an open stage and starts growing again.

## 5. What this decision does not settle

- **The exact size of the citation set.** §1 gives four grep partitions, not a classification;
  telling `0008` §4.11 from `0007` §4.1 takes a read per site. That residue is the resolver's
  subject and the reason it is step 1 rather than step 4.
- **Whether §4's 2803 lines are mostly frozen measurement, mostly status, or mostly taxonomy.**
  §4.11 demonstrably mixes all three in one subsection. Measuring the distribution across
  thirty subsections costs what the partition itself costs, and this decision is constructed so
  that the measurement is not needed.
- **The order of this decision's step 1 against option A's reordering.** A's diff is pure
  movement and would bury step 1's review. They are two pull requests; which goes first is open.
- **`pl-jobs-lora/docs/index.html:83`** — a published page citing `0007` §4.1. Recorded in
  §1.1, owned by no row here.
- **The `0008` collision is portfolio-wide and §0 names its smallest instance.** Three siblings
  carry a decision document of their own at that number —
  `ab-lab/docs/decisions/0008-cluster-robust-variance.md`,
  `apply-scout/docs/decisions/0008_grounding_the_report.md`,
  `mlops-car-price/docs/decisions/0008-serving-an-alias.md` — so a bare `0008` is ambiguous
  across the portfolio and not only across `docs/`. An index-only resolver cannot reach them
  and this decision does not try; it is recorded so the next reader does not find it twice.
