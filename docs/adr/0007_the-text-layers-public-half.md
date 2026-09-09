# The text layers, public half — what S8a contains, and where it splits

Date: 2026-09-09
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: `../audit/0008_the-rollout-ledger.md` §4 (L3, accepted), §4.1 (the refuted cost case),
§4.11 (S8's re-derived scope and the S8a/S8b split), §5 (the README residual);
`../audit/0009_the-review-of-the-whole-system.md` §9, §14, §7 row 11 (the landing surface);
`../audit/0006_session3-4-presentation-block.md` §2.3 (the four About codes), §3 H3, §3 M4;
`../audit/0003_portfolio-review-plan.md` §2's scope table (line 31, the four layers);
`../audit/0007_divergence-and-the-page-spec.md` §5 clauses 4 and 6, §5.0;
`0004_what-carries-the-page-spec.md` §5

*Cite this as `ADR-0007`. Bare `0007` means the page spec in `docs/audit/`.*

---

## 1. The decisions

**D1. S8a's population is every public surface that publishes a portfolio code — 26 committed
sites across all twelve repositories, plus four GitHub About descriptions — not the eight READMEs
the row implies.**

`0008` S8a reads *"the four About codes and their README twins"*; §4.11 re-derived the README half
to eight and never asked the other two layers. `0003` §2's scope table (line 31) had scoped
**four**: *index README, GitHub About + topics, per-project READMEs, live-site headers*. The
live-site layer was lost between `0006` §2.3, which measured About alone, and §4.11, which measured
README and `CLAUDE.md`.

§2.3's argument is that *a recruiter cannot decode the codes*. That argument reaches a **published
page** hardest of all, and three pages put a code in the `.eyebrow` — the first line a reader
meets. A stage that took the eight READMEs would have left every one of them.

*This ADR's layer set is not `0003`'s. It replaces `0003`'s "index README" layer — which W3 handles
as part of L3 and H3 rather than as a code sweep — with a **package docstring** layer `0003` never
scoped.*

**Where that layer stops, stated because the next sweep will otherwise re-derive it.** A package's
`__init__.py` docstring is its published `__doc__` — what `help()` prints, and the first line the
package presents — so it is a public surface and it is S8a's. A docstring inside a module is read
by someone already in the code, which is `CLAUDE.md`'s audience and therefore **S8b's**. The line
is the S8a/S8b split's own, applied one layer deeper: by argument, not by file type. It leaves
eight module-docstring sites to S8b, named in §5.

**D2. The L3 renumber reaches `pl-review-sense/CLAUDE.md:8` and `token-budget/CLAUDE.md:7`, and
those two lines ride in their own repository's S8a pull request.**

They carry the two codes L3 moves (B4→B3, B5→B4) and they sit in **S8b's** population, so the
split appears to forbid taking them. It does not: the S8a/S8b split is by **argument**, and the
argument here is M4's — no two surfaces of one repository may contradict each other — which holds
whatever S8b later decides about a code's usefulness to a contributor. `0008` §4.1's erratum
records this exact pair going stale once already and being repaired in §4.10's round.

**D3. C3 leaves S8a and becomes S8c, and S8c is about the page rather than the headline.**

C3 asked for `pl-review-sense` to *"lead with the challenge set rather than with the benchmark"*.
Two facts settle how, and neither was in the row.

First, the headline is **derived**, not typed: `src/pl_review_sense/site/build.py:88 _headline()`
is a three-state rule with a documented precedence, guarded by `tests/test_site.py:195, :211,
:261, :288`. The adversarial headline **is state 2 and is already implemented**; it does not fire
because state 1 preempts it.

Second, state 1 preempts it **because it won**: HerBERT reaches macro-F1 0.986 against the
baseline's 0.944, McNemar p = 3.1e-06, and `_headline`'s own docstring says *"once HerBERT has run,
the paired test is the strongest thing on the page and leads."* Inverting that precedence would
make the page lead with the **baseline's** probe failure — `analysis.probe()` calls
`baseline.predict` at `analysis.py:155` — burying a significant two-model result behind a
one-model one. It would also move the conformance table, since clause 4 prints the `h1`.

**So S8c leaves `_headline` alone and takes C3's actual intent** — the adversarial set is the
repository's most distinguishing artifact and a reader who does not scroll never meets it — as a
question about the page's own prominence, not its `<h1>`. C3's original copy is separately
unpublishable: `probe()` scores one model, so *"what negation and stripped diacritics do to both
models"* is a figure no committed artifact prints, which is `0007` §5.0 and the trap `0008` §4.2
records for S4. Scoring HerBERT on the challenge set remains available, unscheduled, and costed as
the project it is rather than smuggled into a text stage.

**D4. The replacement copy drops the code and keeps the sentence, and the shape is a precedent
rather than an invention.**

`auth-log-scan/docs/index.html:534` already reads *"Portfolio proof: Linux and security
fundamentals, log analysis, and a pure core…"* — the same sentence with no code. Seven of the eight
own-code READMEs make the code the subject of their opening sentence, so this is one decision
applied eight times rather than eight opening sentences rewritten. The three eyebrows keep their
element — clause 4 gates its **presence** and its text is free — and lose the code:
`mini-traceroute` becomes `Portfolio proof · C++17 · raw sockets`.

**D5. Cross-references become the project's name, not nothing.**

Ten sites say a code about *another* repository, all of them `mlops-car-price` naming
`car-price-ml` as `A3`: `README.md:79, 209, 338, 342, 350, 381`; `docs/index.html:92`
(*"(project A3)"*, in the `<p class="sub">` under the headline) and `:159` (*"the A3 model"*); and
`src/mlops_car_price/__init__.py:1` and `:4`, the package docstring. §2.3's argument reaches them
identically — `A3` is undecodable — and the repair is not a deletion: `MLOps on top of A3` becomes
`MLOps on top of car-price-ml`, which is shorter to read and names something a reader can click.
`pl-jobs-lora/src/pl_jobs_lora/config.py:3` already shows the solved shape — it writes *"the P1
mlops-car-price pattern"*, where the name beside the code is what makes the code redundant.

**D6. H3 is taken on both layers in one copy pass, figure-free, and the profile README's other two
findings are recorded rather than repaired.**

H3's finding is precisely that the index and the profile do not say the same thing about
`apply-scout`; editing them in separate sittings is how that happened. The new sentence names the
retrieval evaluation and the attack surface without digits. Quoting `apply-scout`'s own *"8 of the
27 requirements a repository can prove"* would be legal under §5.0 — its page has printed it since
S3 — but it would add a **third** unguarded figure to the one surface no instrument carries, and
`0009` §14.3 records that surface already quoting `25–66%` rounded past its artifact. `0009` §7
row 11's provenance reader is what earns the right to print a figure there.

**D7. The stage adds no new instrument, and if S8b keeps the codes the guard it then wants must be
built on the code set rather than on a phrase.**

S8a's population is being deleted, so a permanent checker would guard an empty set — unless S8b
keeps the codes in `CLAUDE.md`, in which case the copy source that put them on public surfaces
stays live. §5 states that conditional guard, and §2.2 is why its corpus matters more than its
existence.

## 2. What is measured

Every figure comes from a command. `CLAUDE.md`'s rule, and §2.2 is what it costs to break it.

```
rg -no '\b(A[1-3]|B[1-5]|P[1-5])\b' */README.md | grep -v '^doc-extract/'   # 14
rg -no '\b(A[1-3]|B[1-5]|P[1-5])\b' */docs/index.html */docs/*/index.html  # 8
rg -no '\b(A[1-3]|B[1-5]|P[1-5])\b' */src/*/__init__.py                    # 4
gh api repos/P0w3r223/<name> --jq .description                                 # 4
```

*Two things these commands had wrong when they were first written down, both found by running
them.* `rg -noE` returns **nothing**: in ripgrep `-E` is `--encoding`, so the pattern was consumed
as an encoding name — the flag was carried over from `grep -E`, where it means the opposite kind of
thing. And `--glob '!doc-extract/README.md'` does **not** filter paths given to `rg` as positional
arguments, so the decoy exclusion silently did not happen; the sweep returns 23 and the decoys are
dropped by path instead. *A document whose rule is that every figure comes from a command is worth
exactly as much as the command being run once.* The nine excluded lines are `doc-extract`'s own
evaluation baselines, named in full below.

| layer | own code | cross-reference | sites | repositories |
|---|---|---|---|---|
| README | 8 | 6 | **14** | 9 |
| published page | 6 | 2 | **8** | 5 |
| package docstring | 2 | 2 | **4** | 3 |
| **committed** | **16** | **10** | **26** | **12** |
| GitHub About | 4 | — | **4** | 4 |
| `CLAUDE.md`, L3's two (D2) | 2 | — | **2** | 2 |

**Every one of the twelve repositories publishes a portfolio code somewhere.** The union of the
committed layers is not eleven repositories and not eight.

| own-code sites | where |
|---|---|
| README, 8 | `wroclaw-air-insights:15` A1 · `it-job-radar:14` A2 · `car-price-ml:8` A3 · `mini-traceroute:13` B1 · `auth-log-scan:11` B2 · `pl-review-sense:8` B4 · `token-budget:6` B5 · `pl-jobs-lora:6` P4 |
| page, 6 | **eyebrow, the page's first line**: `mini-traceroute:19` B1 · `ab-lab:146` P2 (← generator `sitegen/page.py:328`) · `doc-extract:175` P5 (← generator `docs/build_index.py:1838`). **footer, beside the gated clause-6 back-link**: `ab-lab:439` P2 (← `sitegen/page.py:292`) · `mlops-car-price:166` P1 · `pl-jobs-lora:244` P4 |
| package docstring, 2 | `apply-scout/src/apply_scout/__init__.py:5` — the code **and** `(the flagship)`, a claim `0004` §5 withdrew · `doc-extract/src/doc_extract/__init__.py:1`, which is the package's entire one-line `__doc__` |
| cross-reference, 10 | `mlops-car-price/README.md:79, 209, 338, 342, 350, 381` · `docs/index.html:92, 159` · `src/mlops_car_price/__init__.py:1, 4` — all `A3`, all naming `car-price-ml` |

**Decoys, excluded and named so a pattern replace never reaches them.** Four corpora, not three.
`doc-extract/README.md` carries nine `B0`–`B3` hits (`:211, 507, 508, 509, 520, 523, 524, 525,
529`) that are the **baselines of its own evaluation**; `doc-extract/CLAUDE.md` carries the same
names, `B0` at `:66` among them; and the same names are **load-bearing in that repository's
source** — `src/doc_extract/eval/baselines.py`, `corrupt.py`, `pattern.py` and `docs/build_index.py`
— where an edit changes behaviour rather than copy. `apply-scout/eval/cassettes/*.jsonl` are
recorded API responses where an edit invalidates a run. Every edit in this stage is made **by named
site from the table above**, never by pattern.

**The four About descriptions, frozen 2026-09-09 before any edit and again after W2** — the
substitute for an instrument on a surface that has none, and the only record this layer gets:

| repository | before | after, written 2026-09-09 |
|---|---|---|
| `mini-traceroute` | `A traceroute written from scratch in C++ over raw sockets (UDP probes + ICMP). Portfolio proof B1.` (98) | `A traceroute written from scratch in C++ over raw sockets (UDP probes + ICMP) — and a page that runs the same checksum, header parser and reply-matching rule in front of you.` (174) |
| `auth-log-scan` | `Scan OpenSSH auth logs for brute-force, user enumeration, and suspicious logins. Portfolio proof B2.` (99) | `Scan OpenSSH auth logs for brute-force, user enumeration and logins that succeed from an address that had been failing — 108 failed logins in 7.1 hours, and only some of them are an attack.` (189) |
| `pl-review-sense` | `Polish review sentiment (3-class): TF-IDF baseline vs HerBERT fine-tuning on PolEmo 2.0. Portfolio A4.` (101) | `Polish review sentiment (3-class) on PolEmo 2.0 — HerBERT reaches 0.986 macro-F1 against a TF-IDF baseline's 0.944, right on 38 reviews it misses and wrong on 7 it gets, p < 0.0001.` (181) |
| `pl-jobs-lora` | `P4: QLoRA fine-tune turning Polish IT job-posting prose into structured JSON, with a self-built dataset and an honest accuracy x cost x latency comparison vs API baselines.` (169) | `QLoRA fine-tune turning Polish IT job-posting prose into structured JSON, with a self-built dataset and an honest accuracy × cost × latency comparison against API baselines.` (173) |

**Every figure in the "after" column is printed by that repository's own `docs/index.html`, and
each was checked against the file before it was written.** `108 failed logins in 7.1 hours` and
`HerBERT reaches 0.986 … 0.944` are those pages' `<h1>` verbatim; `38`, `7` and `p < 0.0001` are
`pl-review-sense`'s lead, which encodes the comparison as `p &lt; 0.0001` — a grep of the raw
markup for `p < 0.0001` returns nothing and that near-miss is why the check was made against
parsed text. `0007` §5.0 has **no carrier on this surface**, so the check is the only thing
standing between it and a figure no artifact prints.

Three of the four descriptions ended on the code as an appended tag, so deleting it alone would
have left a sentence that says nothing about the project; the freed characters carry a measured
claim instead, which is what six of the twelve already did. `pl-jobs-lora`'s change is the
smallest — the code was its **first two characters** — and its `x` becomes the `×` its own README
already writes.

Two are worse than *stale*. **`pl-review-sense` publishes `A4`, and `A4` is not a code in this
portfolio**: Level A ends at `A3` (`README.md:25-27`). Its own README reads `B4`. And
`pl-jobs-lora`'s code is the **first two characters** of its description, so it is the first thing
a reader meets on the repository card.

Not measurable from a working tree, and therefore re-read at W0 of every future pass: the four
descriptions above, and the profile README at `P0w3r223/P0w3r223` — a thirteenth repository
carried by no clause, no test and no row of `SURFACES`.

### 2.1 Corrections to the record, stated rather than applied

- **`0006` §3 H3 cites index `README.md:44`.** That line is now the Level P table header. The
  `apply-scout` row is **`:48`** and the same claim repeats compressed in the pin list at **`:56`**.
  Two sites, not one.
- **`0003` §11 closed `0005` §9's `apply-scout` row** on the grounds that *"neither its README nor
  its `CLAUDE.md` says it"*. `src/apply_scout/__init__.py:5` still does, with the withdrawn
  flagship claim attached. A row closed against two layers of three — `0006` §3 H1's class.
- **`0009` §14.2's *"six of the twelve are linked from it"*** is wrong as stated. Verified
  2026-09-09 against the profile README (unchanged since 2026-09-03): **all twelve are reachable**;
  the six in its "not linked" row each appear in the *Live demos* table as a bare
  `https://p0w3r223.github.io/…` URL, which GFM autolinks. What its table counts is **repository**
  links, and there the split holds — six get a `github.com` link, five of them as a described row
  in the main table and `token-budget` as a bullet under *Also on the profile*.

### 2.2 The correction this document owes on itself

**The first draft of this ADR, corrected before it was merged, counted the page layer with the
phrase `Portfolio (project|proof)` and reported four page sites in three repositories.** The
measured figure is **eight sites in five**, and the four it missed divide into two classes:

- **Two write the bare code with no word between** — `ab-lab:146` (`Portfolio P2`) and
  `doc-extract:175` (`P5` alone), which the phrase cannot match.
- **Two are cross-references** — `mlops-car-price:92` and `:159` — which the phrase could not see
  either, and which the draft had no category for until D5.

Two consequences followed and both were load-bearing:

- **`ab-lab/docs/index.html:146` is an eyebrow** — the page's first line, and the exact site-shape
  D1 uses to argue the page layer belongs in the stage at all. An edit that took only the footer
  would have left the code in the first line of the page, with `ab-lab`'s byte-diff guard green,
  because that guard compares the page to its generator and the generator would have been edited to
  match.
- **`doc-extract` was reported as publishing no code publicly.** It publishes `P5` in its eyebrow.
  The stage's repository count was eleven and is twelve.

*The document that says "figures come from an instrument, not from a hand count" chose the wrong
instrument: a phrase census over a population defined by a code set. Found by the review of that
draft, and it is the same class as the defect the stage exists to fix — a sweep that looked
complete because every site it found was real.*

**And this section got its own correction wrong on the first attempt**, naming `ab-lab:439` among
the bare-code sites when `:439` reads `Portfolio project P2` and the draft's phrase census had
found it. Caught by the re-review. *An erratum is a measurement like any other and it was written
from memory of the diff rather than from the file — which is the same failure one layer up, in the
paragraph whose whole subject is that failure.*

- **A third correction the same error produced.** That draft's §2.1 asserted that `0008` §4.11's
  false-positive warning names `doc-extract/README.md:507-529` *"only"*. It does not: §4.11 also
  names `:211`, `:520` and `:523`, and ends **on `main`** with *"Separately,
  `mlops-car-price/README.md` uses `A3` six times as a live cross-reference."* The cross-reference
  class the census dropped was one the record already held, and D5 now owns it.
- **A fourth, found only when the re-review asked why one layer had not been re-swept.** The
  package layer kept its original instrument — a literal lookup for one known string in one known
  file — through the very commit that replaced the phrase census everywhere else. Re-run on the
  code set it is **2 own-code sites, not 1**: `doc-extract/src/doc_extract/__init__.py:1` publishes
  `P5` as its entire `__doc__`. *The fix to a wrong instrument was applied to the layers that had
  already failed and not to the layer that had not been checked* — which is how a repair leaves the
  same defect standing one file away.

## 3. Sequencing

**Twelve sibling pull requests, four account edits, one index pull request and one on the profile.**
The index re-points; it never edits a submodule.

| wave | what | parallel | gate |
|---|---|---|---|
| **W0** | Entry state; freeze the four About descriptions **into this document before touching one**; save `python -m tools.pagespec --detail` as the baseline | — | `0008` §6, all rows. **Done 2026-09-09**: §2 above, zero `FAIL`, zero open pull requests across fourteen repositories |
| **W1** | Twelve sibling pull requests — one per repository, covering all 26 committed sites and D2's two `CLAUDE.md` lines | **yes, fully independent** | each repository's own CI, plus §3.1's two guards. **Done 2026-09-09** — twelve merged: `mini-traceroute` #8 · `doc-extract` #14 · `auth-log-scan` #12 · `car-price-ml` #30 · `it-job-radar` #35 · `wroclaw-air-insights` #40 · `token-budget` #5 · `apply-scout` #37 · `pl-review-sense` #19 · `pl-jobs-lora` #17 · `ab-lab` #20 · `mlops-car-price` #24. The census over all three committed layers reads **zero** |
| **W2** | The four About edits, **each immediately after its own repository's W1 merge**, never batched — the reviewable artifact lands first and the account window closes in seconds | per repository | none exists; the before/after in §2 *is* the record. **Done 2026-09-09**, after all twelve W1 merges rather than one at a time, because W1 completed in a single sitting and the window the row guards against never opened. Read back from the account and verified: zero codes, every figure sourced, `—` is U+2014 and `×` is U+00D7 |
| **W3** | One index pull request: twelve pointer bumps + L3 (`README.md:29-37`) + H3 | after W1 | `pagespec` runs, and the conformance table must be **byte-identical** against the W0 baseline — no page's verdict may move |
| **W4** | The profile README pull request — H3's public half | with W3 | review only; nothing carries this surface |
| **S8c** | C3's intent, its own sibling pull request, then a second index bump | later | `--only pl-review-sense` clear before the bump, `--fetch` after Pages deploys |

**Why siblings before the index.** The moment `README.md` says `B3 = pl-review-sense` while that
repository still publishes `B4`, the index and a repository disagree about the same project.
Deleting the codes first is also what makes L3's renumber free, which is `0008` §4.1's erratum
holding as written and reproducing today.

**H3's two index line numbers shift when L3 deletes B3's row**, so W3 edits L3 first and re-reads
`:48` and `:56` rather than citing them from here.

### 3.1 Two sibling guards go red on a correct edit, and that is the stage's own business

`mlops-car-price/tests/test_docs_page.py:54` and `pl-jobs-lora/tests/test_docs_page.py:62` each
carry `(r"\b[AP]\d\b", "the portfolio's own ranking codes…")` as a provenance-check exemption, and
each runs `test_the_exemptions_are_shapes_that_still_fire_where_they_are_applied`, whose body is
`assert tally.get(pattern)`. Delete the codes and the exemption stops firing, so **both pull
requests must delete the exemption in the same commit as the copy.** No other sibling carries this
shape; `ab-lab` and `doc-extract` do not.

D5 is what makes `mlops-car-price` unambiguous: its page holds three `[AP]\d` sites (`:92`, `:159`,
`:166`) and all three go, so the exemption is dead rather than half-dead. Had the cross-references
been left, that guard would have stayed green over them and the stage would have read as complete.

### 3.2 Three mechanism notes, so the stage does not learn them on the day

`README.md` is **not** in `pagespec.yml`'s `paths:` filters, so a README-only index commit gets no
run at all — the absence is the filter working, as with `b416c83`. W3 bumps pointers, so its run
fires. `token-budget` is not among the eleven filter names because it carries no `Surface`
(`sources.py`: twelve surfaces, eleven repositories, `car-price-ml` twice), and the other pointers
in the same commit trigger the job. And **the eleven/twelve trap does not arm here**:
`wroclaw`'s only site is its README, no clause enters `GATE`, and no `pending` row is needed.

## 4. Risks

| risk | control |
|---|---|
| Three page edits sit beside the clause-6 back-link, which is **gated** | clause 6 counts *anchors*, so removing footer **text** cannot move it; `python -m tools.pagespec --only <repo>` before the pointer bump confirms it per repository |
| Three page edits are in an `.eyebrow`, whose presence clause 4 gates | the code is removed from **inside** the element; the element is not touched |
| `ab-lab` **and `doc-extract`** are byte-diffed against their generators — `ab-lab`'s two sites have two different generator lines (`page.py:292` and `:328`), and `doc-extract`'s eyebrow comes from `docs/build_index.py:1838` | generator and page in one commit, both `ab-lab` sites in the same edit; `--only ab-lab` and `--only doc-extract` after |
| `mini-traceroute` holds no Python and therefore **no local page test**, so the index checker is its only guard | `--only mini-traceroute` after the edit, before the pointer bump |
| A pattern replace corrupts the three decoy corpora named in §2 | edit **by named site**, never by pattern — and §2.2 is what a pattern chosen for convenience already cost |
| The About layer produces no reviewable artifact | §2's frozen before/after, and W2 landing per repository rather than batched |

## 5. Consequences

- **S8b's scope changes in four ways.** Two of its twelve `CLAUDE.md` will already carry their
  post-L3 code (D2); its decoy corpus is larger than §4.11 records (§2.2); the recruiter argument
  is settled on every public layer, so S8b decides only the contributor question `0008` §4.11
  framed; and **D1's boundary hands it eight module-docstring sites** —
  `mlops-car-price/src/mlops_car_price/dataset.py:3, :83` and `training/train.py:12, :70`
  (cross-references), and `pl-jobs-lora/src/pl_jobs_lora/config.py:3`, `tracking.py:3`,
  `normalize.py:4`, `vocab.py:4`. They are named here so S8b does not sweep for them a third
  time.
- **If S8b keeps the codes**, this ADR recommends one `submodules`-marked test in the index
  asserting that no sibling README, published page or package docstring publishes a portfolio code.
  **Its corpus must be the code set `\b(A[1-3]|B[1-5]|P[1-5])\b`, not a phrase**, and its mutation
  proof must use a code with no word beside it — otherwise it ships green over exactly the two
  sites §2.2 records, which is `CLAUDE.md`'s "at least seven guards that shipped green over the
  defect they existed to catch" with the mechanism named in advance. It would be the first index
  test about something other than the page spec, which is why it is conditional. **If S8b deletes
  them too**, add nothing.
- **`0009` §7 row 11 is unaffected in priority and better positioned in fact.** After W4 the
  profile's `apply-scout` claim matches its repository, so row 11's future instrument starts
  against a surface with one fewer known defect and no new figure (D6).
- **Explicitly out of scope**: a §5.0 sweep of the whole index README (§4.10 did that round);
  `0009` §14.2 and §14.3, which belong to row 11; and `0008` §5's README-provenance reader.
