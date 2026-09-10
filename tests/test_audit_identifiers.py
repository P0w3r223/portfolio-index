"""Guards for the audit's identifier template, `0010` §3.2.

The template is **tracked**, and the file it is a template for holds the owner's private
identifiers and must never be. Two prose claims carry that arrangement — *"placeholders and
no identifier"* and *"the ignore pattern names an exact filename"* — and this repository's
rule is that a claim of that shape becomes an instrument or it decays. These are the
instrument.

The failure mode is not exotic. The template sits at the root under a name one keystroke from
the real one, so the cheap mistake is filling it **in place**: `git status` then shows an
ordinary modified tracked file, nothing objects, and `git add .` commits a PESEL. The first
two guards below are the ones that go red on that, and they go red before the commit rather
than after it.

The fourth reads the sibling trees and is why it carries the marker. `.gitignore` is *this*
repository's file and git does not descend into submodules, so `audit-identifiers.local`
inside `ab-lab/` is ignored by nothing — and every one of the twelve is public. Sessions 1–12
each work with a submodule directory open, which is exactly where a relative copy lands
wrong. Verified when this file was written: `git -C ab-lab check-ignore audit-identifiers.local`
exits 1.

**What makes this portable across line endings is `read_text`, not `splitlines`** — and the
first version of this paragraph said the opposite, in both halves. `Path.read_text` opens in
universal-newline mode, so CRLF is folded to `\\n` before anything splits and `.split("\\n")`
would behave identically; `0010` §3.6 observation 5 says the same thing from the other side.
`splitlines()` is kept because it drops the trailing empty element and says so at the call
site. The tree itself is the other way round from what that paragraph claimed: `core.autocrlf`
is `true` here and there is no `.gitattributes`, so the working file holds **50 CRLF** and the
blob holds **50 bare LF** — measured, not assumed.

Neither guard's `paths:` trigger was in the workflow when they were written, so the two
single-file changes that redden them — filling a value, widening the ignore — would have run
no CI at all. `.gitignore` and the template are in both filters now; `_A_REPOSITORY` in
`tests/test_sources.py` matches neither, so the registry guard is unaffected.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from tools import entry_state

ROOT = Path(__file__).resolve().parents[1]

#: The working copy the audit reads. Never tracked, anywhere in the portfolio.
WORKING_COPY = "audit-identifiers.local"
#: The committed template, whose whole safety argument is that every value is still this.
TEMPLATE = ROOT / "audit-identifiers.local.example"
PLACEHOLDER = "<fill in or delete this line>"
#: The trigger that decides whether any of this runs in CI at all.
WORKFLOW = ROOT / ".github" / "workflows" / "pagespec.yml"


def _check_ignore(path: str) -> int:
    """`git check-ignore --no-index`, and the exit code it is safe to read as an answer.

    The command answers 0 for *ignored* and 1 for *not ignored*, and **128 for an error** —
    a broken repository, a bad flag, a git too old for `--no-index`. Returning 128 unchecked
    would let a failing command read as *not ignored*, which is a real verdict here: the
    template assertion would pass on it and the working-copy assertion would redden with a
    diagnosis about `.gitignore` that names the wrong cause. So 128 is refused rather than
    interpreted, `ls-files` already does the same on its own call, and the two assertions
    above stay free to read 0 and 1 as the answers they are.
    """
    done = subprocess.run(("git", "check-ignore", "--no-index", path), cwd=ROOT,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")

    assert done.returncode in (0, 1), (
        f"`git check-ignore --no-index {path}` exited {done.returncode}, which is neither "
        f"answer: {done.stderr.strip() or 'no stderr'}"
    )
    return done.returncode


def _values() -> list[tuple[str, str]]:
    """Every `key = value` the template declares, comments and blank lines dropped.

    Split on the **first** `=` only. A value is free text by `0010` §3.2 and may contain one;
    splitting on all of them would silently drop the tail and score a filled line as empty,
    which is the direction that matters here.
    """
    pairs = []
    for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        pairs.append((key.strip(), value.strip()))
    return pairs


def test_the_template_declares_keys_at_all():
    """The floor under the guard below, and it is not redundant.

    An empty file satisfies *"every value is a placeholder"* vacuously, so a template gutted
    to a comment header would pass the identifier guard while telling a reader nothing about
    the form. `0008` §3.6's observation 1 in file form: a check that collected nothing reads
    exactly like a check that passed.
    """
    assert len(_values()) >= 1


def test_no_value_in_the_committed_template_is_an_identifier():
    """`0010` §3.2's *"safe by construction"*, made an instrument rather than a sentence.

    This is the guard that reddens when the template is filled **in place** instead of being
    copied — the one mistake its location makes cheap. It asserts the placeholder exactly, not
    merely that the value is short or looks unlike an e-mail: a rule that tries to recognise an
    identifier is a rule that will one day fail to, and the value here is under our control.
    """
    filled = [(key, value) for key, value in _values() if value != PLACEHOLDER]

    assert not filled, (
        f"{TEMPLATE.name} carries {len(filled)} filled value(s) — "
        f"{', '.join(key for key, _ in filled)}. Copy it to {WORKING_COPY} and fill the copy; "
        "this file is tracked."
    )


def test_the_working_copy_is_tracked_by_nothing_in_the_index():
    """The other half, and the half the template's own text cannot promise.

    `git ls-files` and not `git check-ignore`: they answer different questions, and it is
    tracking that leaks. A file can be untracked and unignored — the ordinary state of a fresh
    working copy — and this guard stays green over that, correctly. What it refuses is the
    committed one.
    """
    tracked = subprocess.run(("git", "ls-files", "--", WORKING_COPY), cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8",
                             errors="replace")

    assert tracked.returncode == 0
    assert tracked.stdout.strip() == "", (
        f"{WORKING_COPY} is tracked in the index. It holds the owner's private identifiers "
        "by design — `0010` §3.2."
    )


def test_the_ignore_reaches_the_working_copy_and_not_the_template():
    """Both directions, because each has its own way of going wrong.

    Widening the pattern to `audit-identifiers.local*` would swallow the template and make it
    untrackable; dropping the line would leave the filled copy one `git add .` from a commit.
    A test asserting only the first direction passes over the second, which is `0009` §5.1's
    shape — a ratchet guarded one way.

    **`--no-index`, and the first version of this test did not pass it.** Without the flag
    `git check-ignore` skips paths already in the index — tracked files are not subject to
    exclude rules, so it answers *not ignored* for the template whatever `.gitignore` says.
    The template is tracked, so that assertion could not fail: it went green over the glob
    mutation written to redden it. Found by the battery, which is the only reason it was
    found at all — the guard read correctly, ran, and proved nothing. `--no-index` asks the
    question the docstring claims to ask: does the pattern *reach* this path.
    """
    ignored = _check_ignore(WORKING_COPY)
    template = _check_ignore(TEMPLATE.name)

    assert ignored == 0, (
        f"{WORKING_COPY} is not ignored — the `.gitignore` line naming it exactly is gone, "
        "and a filled copy is one `git add .` from a commit"
    )
    assert template == 1, (
        f"{TEMPLATE.name} is ignored, so it cannot be committed — the pattern has been "
        "widened past the exact filename"
    )


def test_both_workflow_filters_name_the_two_files_these_guards_read():
    """The trigger, which is the half a guard cannot supply for itself.

    Every other guard here is about the files; this one is about whether anything runs them.
    Two of the mutations that prove this module are single-file changes to `.gitignore` and to
    the template, and until 2026-09-10 neither path was in either `paths:` list — so both
    reddened locally and would have run **no job at all**. There is no pre-commit hook, so
    nothing else stood between that edit and `main`.

    **`test_sources.py`'s registry guard cannot cover this**, and the reason is structural
    rather than an oversight: its `_A_REPOSITORY` is `^[^/.]+$`, so an entry carrying a dot is
    not a repository and is dropped before its equality check ever sees it. Both of these
    entries carry one. That is what keeps them from breaking the `SURFACES` comparison, and it
    is exactly what leaves them unwatched — so this assertion is where they are watched.
    """
    lists = re.findall(r"paths:\s*\[(.*?)\]", WORKFLOW.read_text(encoding="utf-8"), re.S)

    assert len(lists) == 2, (
        f"expected a `paths:` filter on push and on pull_request, parsed {len(lists)}; "
        "the workflow's shape moved under this guard"
    )
    for index, block in enumerate(lists):
        named = {raw.strip().strip("'\"") for raw in block.split(",")}
        for needed in (".gitignore", TEMPLATE.name):
            assert needed in named, (
                f"`paths:` filter {index + 1} of 2 does not name {needed}, so a change to it "
                "runs no CI job and the guards in this file cannot see the edit that breaks "
                "them"
            )


@pytest.mark.submodules
def test_no_sibling_working_tree_holds_a_copy():
    """The hazard `.gitignore` cannot reach, in the repositories where it costs most.

    Git does not descend into submodules, so this name inside a sibling is ignored by nothing
    — and the twelve are public. A scan session works with one submodule directory open, which
    is where a relative copy lands wrong, and the file would sit there untracked and unignored
    until somebody's `git add .`.

    Existence and not tracking, deliberately: by the time it is tracked the guard is too late.

    **The sweep enumerates `.gitmodules` rather than globbing `*/.git`.** The first version
    globbed, and `if not checked: skip` refuses only the empty set — so with one submodule
    initialised and eleven absent it passed having looked at one, and read identically to a
    sweep of twelve. That is observation 1 from `0010` §3.6 and the argument this file already
    makes two functions above, walked into anyway. `test_published_surfaces.py` enumerates
    `sources.SURFACES` for the same reason; the registry here is `.gitmodules`, because
    `token-budget` publishes no surface and the hazard reaches it all the same. The count is
    in the message so that a partial run says so instead of looking complete.
    """
    declared = entry_state.submodule_names((ROOT / ".gitmodules").read_text(encoding="utf-8"))
    present = [name for name in declared if (ROOT / name / ".git").exists()]
    found = [name for name in present if (ROOT / name / WORKING_COPY).exists()]

    assert declared, ".gitmodules declares no submodule; the registry moved under this guard"
    if not present:
        pytest.skip(f"none of the {len(declared)} declared submodules is checked out")

    assert not found, (
        f"{WORKING_COPY} exists in {', '.join(found)} — ignored by nothing, and those "
        f"repositories are public. It belongs at the index root and nowhere else. "
        f"(swept {len(present)} of {len(declared)} declared submodules)"
    )
