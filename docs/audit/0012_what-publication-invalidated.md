# What publication invalidated

Date: 2026-09-17
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: [0011](0011_the-pre-publication-security-audit.md) §6 step 0 (the route this document
is the aftermath of) and §7 (the checklist whose executed state is §5 here),
[0010](0010_the-portfolio-audit.md) §3.1 and §6 (the queue whose working repository moved
mid-run), [ADR-0004](../adr/0004_what-carries-the-page-spec.md) §6 (the cost publication
amortised), [0009](0009_the-review-of-the-whole-system.md) §7 row 11 and §14 (the open row whose
measurement went stale the same day),
[failure-classes](../reference/failure-classes.md) family `ST` (what this whole document is an
instance of)

---

## 1. What this is

`0011` §6 route A published this index on 2026-09-17. **Route A changed no byte of `main`** — it
cloned it — so nothing in the tree broke, no test went red, and no instrument said anything. What
changed is the truth value of every sentence whose premise was *this repository is private*, and
those sentences are spread across four kinds of file that are read four different ways.

This document is the list, the corrections that fit in one pass, and the reasons for the ones that
do not. It is **not** a security audit: `0011` is that, it verified the published clone against the
server rather than against a local copy, and nothing in §4 below is an exposure.

**Why it needed to exist rather than happening during the move.** The move itself found four
things it had not costed, all of them live: `tools/entry_state.py`'s `INDEX` was a dependency on
the repository's own name, the fresh clone's git identity was *empty* rather than wrong, required
status checks were missing from a ruleset that already required a pull request, and `approvals: 1`
made every future pull request unmergeable for a solo owner. Those were caught because they
**failed visibly** within minutes. Everything in §4 fails invisibly, which is why it takes a
document and not a debugging session.

## 2. The class, stated once

A publication is a `ST`-family generator with an unusual property: **the defect arrives without a
commit.** The ordinary `ST` case is a sentence that describes work and then the work moves. Here
the sentence did not move and the work did not move; the *world outside the repository* moved, and
the sentence's premise moved with it.

That makes it invisible to everything this repository owns:

- `python -m pytest` asserts properties of the checker and of the committed surfaces. A comment's
  premise is not a property.
- `python -m tools.citations` resolves a `§N` to a heading and stops. It answers *does this section
  exist*, never *does it still hold* — the blind spot named on 2026-09-17, and it is exactly the
  one that matters here.
- `python -m tools.spec` pins every normative sentence of `0007` §5–§6 **by literal**. It is
  therefore the one instrument that would notice if such a sentence were *edited* — and it is
  silent when the sentence stays byte-identical and stops being true. §4's F-1 is that case, and
  the pin makes the repair more expensive rather than less.
- `git grep` finds the string `private`. It cannot tell a sentence asserting privacy from one
  describing the archive correctly, and §4's F-7 is a guard where the distinction is the whole
  finding.

**So the instrument is reading, and the unit is the premise.** `0010` §5 records three shapes found
by a `code-reviewer` pass that a mutation battery structurally cannot see; this is a fourth, and
unlike those three it has no instrument at all rather than the wrong one.

## 3. What was read, and what was deliberately not

Read: every tracked file outside `docs/audit/` for the premise *private index*, the twelve
submodule working trees at their pinned gitlinks for the same, `0007` §5–§6 against
`tools/spec.py`'s pins, `0009` §7 and §14, and the live repository settings through the GitHub API.

Not read for this purpose: `docs/audit/0001`–`0011`. `README.md` exempts them and the exemption is
right — a dated record is supposed to read as it was written. **That exemption is now stated as
covering them alone**, because for one day it was read as covering the tree.

Figures below carry the command that produces them. Sweeps use `git grep` and `git ls-files`,
never `grep -r` or a filesystem walk: `0010` §6's row of 2026-09-11 records what that cost once,
and the twelve trees have gitignored build output no clone has.

## 4. Findings

| # | what | weight | state |
|---|---|---|---|
| F-1 | `0007` §6 `c9.s2` — a **normative** sentence arguing from the private index, pinned by literal in `tools/spec.py` | **highest** | open — design decision, `0009` §7 row 11 is the same question |
| F-2 | `.github/workflows/pagespec.yml` said the decision was open and this repository stays private | high | **corrected here** |
| F-3 | `ADR-0004` §6 still carried a cost publication amortised | high | **corrected here** |
| F-4 | `0010` §3.1, §3.3 and both prompts named the archive as the working repository | high | **corrected here** |
| F-5 | `README.md`'s non-retrofit notice read as covering the whole tree | medium | **corrected here** |
| F-6 | `0009` §14's profile measurement predates the profile edit of 2026-09-17 | medium | open — it is F-1's input |
| F-7 | `doc-extract`'s guard: correct assertion, false reason, and no instrument can see it | medium | open — the repository is mid-scan |
| F-8 | 21 lines across the twelve submodule `CLAUDE.md` say *the private portfolio index* | medium | open — needs a decision on where the carrier lives |
| F-9 | `0011` §7's applied state lived only in a gitignored session brief | medium | **recorded here**, §5 |

### F-1 — the normative sentence, and why it is the whole of §6

`0007` §6 clause 9's second sentence reads *"That two pages agree cannot be checked without
coupling two public repositories to a private index, so it is a review item"*, and
`tools/spec.py`'s `c9.s2` pins it verbatim with the carrier *"the clause states its own limit;
this row records that the absence of an index check is the decision and not a gap"*.

**The limit is the premise, and the premise is gone.** Coupling two public repositories to a
*public* index is what `ADR-0004` K-c already does for clauses 1 through 8. So the sentence now
argues from a fact that stopped being true, and the row beside it converts an absence into a
*decision* on the strength of it. That is the most load-bearing place in this repository for this
class of defect to sit: `ADR-0004` §5 accepted `0007` §5–§6 as the one stable normative text, and
everything about what is carried and what is merely reviewed is read off it.

**It is not corrected here, and the threshold is why.** `0010` §3.5 puts a change to `0007` in its
second column — its own row and its own pass — and `tools/spec.py`'s guard searches the pinned
quote inside the `NORMATIVE_FROM`/`NORMATIVE_TO` slice, so the document and its pin must move in
one commit or the suite goes red. More importantly the right repair is not obvious: clause 9 could
become carried, could stay a review item for a different and still-true reason, or could be
rewritten so the limit is about *who renders the surface* rather than about who can read it.

**And it is the same question as `0009` §7 row 11.** That row wants the profile README brought
into the system and is blocked on which clauses can be asked of a surface someone else renders
(§14.1). Clause 9 is blocked on what the index may claim about two surfaces it does not own.
Publication dissolved one of the two blockers and left the other standing. Taking them separately
means two changes to `0007` in two windows, and `0009` §13.6 is the rule about what that costs.
**They are one stage, and it needs `architect` before `@Plan`.**

### F-2, F-3, F-4, F-5 — corrected in this pass

All four are one repository, no new module, no signature, no clause; §3.5's first column.

**F-2**, `.github/workflows/pagespec.yml`: the pinning rationale said the workflow *"is about to
be read publicly"* and then argued in italics that route A was undecided and would leave this
repository private. It is the clone, it is public, and the file saying otherwise is the first thing
a reader of a public workflow meets. Corrected, with the reason the correction did not arrive on
its own — see F-5.

**F-3**, `ADR-0004` §6: the counter-argument bullet said a checker in the *private* index leaves
the twelve public repositories with no visible proof that a spec governs them. Amended rather than
struck, because the bullet is part of the reasoning K-c was accepted on. **What survives is
locality, not visibility**: `mini-traceroute` still carries no assertion of its own and holds no
Python at all, so a reader who clones that repository alone still learns nothing about the spec.
That was always the smaller half of the two the bullet conflated.

**F-4**, `0010`: §3.1's session 13 named the archive, §3.3's command row keyed on it, and **both
prompts** sent a session to branch and commit there — where a commit reaches no reader. Session 4
is the worked instance and this document's §6 is what it needed. The queue's denominator stays
**fifteen**: the archive is outside the corpus and outside the queue, because `0011` is its audit
of record on the axes a scan session could have asked about, and it will not change again.
§2.1's corpus row still names the archive and keeps its figures — §2 is the state the audit was
*opened* against, and re-measuring it is what §4's header refuses.

**F-5**, `README.md`: the notice exempting `docs/audit/` from retrofit is correct and was read for
one day as covering everything. It now says the exemption is theirs alone and names the four kinds
of file that are corrected instead. *This is the finding that explains the other three*: the
exemption is the reason nobody swept `.github/`, `tools/` or `docs/adr/` after the move.

### F-6 — the measurement that a same-day edit invalidated

`0009` §14.1 gives *anchors ending at the profile* as **10**, measured 2026-09-08, and §14.2 splits
them six and six. The profile README was edited by hand on 2026-09-17 to link the published index,
so the figure is at least one low and the split has moved.

**It matters because it is F-1's input.** §14 asks for a scope decision before row 11 is taken, and
taking that decision on the 2026-09-08 figure would be `FG-2` — a figure taken from a document
rather than from the instrument — committed inside the document that names the class. §14.3 says so
about itself already. The re-measurement is one `--fetch` and belongs to the stage, not here:
measuring it now would produce a second frozen figure, and the stage would have to re-take it
anyway.

### F-7 — a guard whose assertion is right and whose reason is false

`doc-extract/tests/test_site_committed.py` asserts that the committed page does not link the index,
with the message *"the index repository is private — a link to it is a 404 for every reader"*, and
its docstring says the same. `doc-extract/docs/build_index.py` repeats the premise.

**The assertion still passes, and that is the finding.** It tests for the absence of
`current_projects`, which is still private, so the guard is green and will stay green. Only the
*reason* is false, and no instrument anywhere reads a reason. This is `0010` §5's amended-ADR
fan-out shape reached from a new direction: there the retired claim survived in prose the ADR could
not reach; here it survives inside the guard's own explanation of itself.

**Not repaired, for two reasons that agree.** `doc-extract` is session 5's subject and a scan
session may not act (`0010` §3.1); and `0009` §13.6 forbids repairing a guard in the window that
guard is carrying a stage. It also raises a question this document cannot settle: with the index
public, the page *could* link it, so the guard may be asserting the wrong thing rather than
explaining itself wrongly.

### F-8 — twenty-one lines in twelve manuals

Every one of the twelve submodules calls this repository the private portfolio index.

```bash
for r in <the twelve>; do git -C "$r" grep -cin 'private \(portfolio \)\?index' -- CLAUDE.md; done
```

Twenty-one lines at the pinned gitlinks: seven repositories carry two apiece, four carry one, and
`pl-review-sense` carries three. Restricting the same sweep to every tracked `*.md` returns the
same twenty-one, so all of them are in `CLAUDE.md` and none is in a README or a dated record.

These are **manuals in the present tense**, so `0010` §5's exclusion list does not reach them — it
covers `docs/adr|plan|ideas|research`. And the repair is an improvement rather than tidying: with
the index public, each sibling can carry a working link to the spec that governs its page, which is
F-3's residual cost paid on the side a reader can see.

**It needs a decision first, and the decision is `architect`'s**, because it is the same one
`0010` §5's last bullet already routes there: twelve repositories cannot each grow a guard for a
claim about the index without twelve new guards, and the index cannot assert a sentence in a file
it does not edit. This repository re-points submodules; it does not edit them.

## 5. The repository state, read from the API

`0011` §7 is a requirement list written before the switch and against a repository it does not
name. This is what is applied to `P0w3r223/portfolio-index`, read back with `gh api` rather than
from anyone's recollection. **Three of these are settings §7 does not name, and two are items §7
names that nothing in the record had answered.**

| setting | state | note |
|---|---|---|
| secret scanning | enabled | §7 |
| push protection | enabled | §7 — the only preventive control on the list |
| Dependabot alerts / security updates | enabled | §7 |
| private vulnerability reporting | enabled | §7 |
| **secret scanning, non-provider patterns** | **disabled** | **not in §7**, and it is the half that catches secrets outside known providers' formats |
| **secret scanning, validity checks** | **disabled** | **not in §7** |
| ruleset on `main` | `active` | `pull_request`, `required_status_checks`, `required_linear_history`, `non_fast_forward`, `deletion` |
| required checks | `checker (no submodules)`, `checker over the published surfaces` | the two jobs a pull request arms; `the live surface` carries an `if:` and skips |
| `required_approving_review_count` | **0**, not §7's 1 | GitHub forbids approving your own pull request, so 1 made every pull request unmergeable for a solo owner. Pull request, both checks, linear history, no force-push and no deletion all still enforced |
| `require_extra_approval_for_unattributed_changes` | **true** | **not in §7**, and see below |
| require branches up to date | not enabled | §7 asks; no answer was on the record |
| require signed commits | not enabled | §7 asks; needs a signing key first, so it is `0011` §6 step 4's shape — the owner's to close |
| deploy keys / webhooks / Actions secrets / environments | 0 / 0 / 0 / 0 | |
| default workflow permissions | `read`, and workflows cannot approve pull requests | |

**`require_extra_approval_for_unattributed_changes` is worth its own paragraph**, because it is the
second instance of a shape this repository has already paid for once. Like `approvals: 1`, it can
make a solo owner's pull request unmergeable — it demands an approval nobody can give when a commit
in the branch is authored by an identity GitHub cannot attribute to an account. It does not bite
today: `p0w3r2243@gmail.com` is linked, so `gh api repos/…/commits/<sha> --jq .author.login` returns
`P0w3r223` for commits carrying it. **What would trip it is precisely R-1's mechanism** — a clone
whose git identity is unset, where git falls back to the machine name. So the flag is at once an
accidental guard against R-1 recurring in a pull request and a trap that would present as an
unexplained block. Left enabled, deliberately, now that it is written down.

*One thing enabling Dependabot does that no file records*: GitHub adds a managed `Dependency Graph`
workflow whose check, `update-pip-graph`, exists in no file in this tree. It is not in the required
set and does not gate.

## 6. A branch stranded by the move

`0010` §6's new row sends a session here. The situation: work committed in the archive after it
stopped accepting commits, on a branch based on an archive commit.

**It transplants, and route A is the reason.** A `filter-repo` rewrite would have changed every
SHA; a clone did not, so the branch's base commit exists in the published index under the same
hash. Two commands settle it before anything is moved:

```bash
git merge-base --is-ancestor <branch base> main            # exit 0: the base is reachable here
git log --oneline <branch base>..main -- <the files it touches>   # empty: nothing conflicts
```

The second is the one that proves something. If it is empty, `git fetch <archive path> <branch>`
followed by `git cherry-pick <base>..FETCH_HEAD` cannot conflict; if it is not, the work needs a
rebase and a reader.

**And the transplanted content needs one correction that is not mechanical.** A row measured in one
repository is read by someone holding another, so every sentence in it whose premise is *this
repository*, *the private index* or an entry state changes truth value without changing a byte —
§2's class, arriving through the same door. Session 4's row is the worked example: its own
publication sentence was falsified by the merge that published it, its `Index SHA` cell does not
meet `0010` §4's definition for a reader here, and the paragraph written to handle exactly this
overreached about what route B would cost. All three are recorded in that row's errata round three,
including the two the round produced while being written.

## 7. What this document does to itself

`0011` §9's rules apply unchanged and are not restated. R-2's four private repository names are
cited by section and not repeated; they are in `main` already, and a fifth site is a fifth site to
redact. R-1's literals appear nowhere — the shape §6 above describes is stated as *the machine
name*, which is what it is.

**Two things this document cannot verify**, stated because a later reader will otherwise assume
they were checked. Whether the profile README's anchor count has moved by exactly one or by more
is F-6 and is deliberately unmeasured. And whether `doc-extract`'s guard should now assert the
opposite is a question for session 5's repair, not a finding this document is entitled to close.

**One figure here invalidates itself on sight and carries no number for that reason**: how many
sentences in this repository still argue from a premise publication changed. The sweep that would
count them matches the word `private`, and this document contains that word more often than any
other file in the tree.

## 8. One thing found while writing this, which is not this document's subject

Three guards in `tests/test_published_surfaces.py` — the ones asserting that a wire failure, a
fallback to the committed file, and an undelivered stylesheet each **skip** the fetching sweep
rather than reddening it — go **red rather than skipping** when run where the submodules are not
checked out. A `git worktree` is that environment: `git worktree add` populates no submodule.

The mechanism is worth the four lines. Each guard wraps the sweep in
`pytest.raises(pytest.skip.Exception, match=…)` and asserts on the message. With no submodule on
disk, the fixture raises a *different* skip first — *"ab-lab is not checked out"* — so the
`raises` catches it, `match` does not, and the failure reads as though the wire degradation were
broken. **The `match=` is what keeps this a false red instead of a false green**: without it, the
guard would swallow the wrong skip and pass while proving nothing, which is family `SG`.

So the guard is well built and its *precondition* is unasserted, which is `0010` §6's 2026-09-14
class — an environment verdict presenting as a repository one. Not repaired here: it is
`tools/`-adjacent test work, unrelated to publication, and §3.5 puts a guard change in its own
pass. **What a reader needs meanwhile**: run `python -m pytest -m 'not submodules'` in a worktree,
and the full suite only where the twelve are checked out. On `main` in such a checkout the suite
is green, which is the measurement that separates this from a real failure.
