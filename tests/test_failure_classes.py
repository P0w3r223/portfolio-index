"""Guards for `docs/reference/failure-classes.md` — `ADR-0009` §3 step 3.

The document's own §2 states the entry rule: a class states **where it was defined**, **where
it recurred**, and **the test** — *"a class with no test is a story"*. A rule with no carrier is
what `0009` §3.2 found landing three times, so the rule gets one here.

Nothing about the prose is asserted. What is asserted is the shape §2 promises, and the ids,
because the ids are the thing other files will cite once step 4 starts migrating citations onto
them. The claims the document makes about *where* a class was defined are guarded elsewhere and
better: they are citations, and `tools/citations.py` resolves every one of them.
"""

from __future__ import annotations

import re
from pathlib import Path

from tools import citations

CLASSES = Path(citations.ROOT) / "docs" / "reference" / "failure-classes.md"

#: `### SG-1 — the guard is green under its own mutation`
_CLASS = re.compile(r"^### ([A-Z]{2}-\d+) — (.+)$")

#: The families §2 allows to grow. Pinned rather than derived, so opening a new one is an edit
#: a reader sees — the shape `NOT_A_SENTENCE` and `GATE` both have, and for the same reason.
_FAMILIES = frozenset({"SG", "ST", "FG", "SC"})


def _blocks() -> list[tuple[str, str]]:
    """Each class id with the body that follows it, up to the next heading of any level."""
    text = CLASSES.read_text(encoding="utf-8")
    out, current, body = [], None, []
    for line in text.splitlines():
        match = _CLASS.match(line)
        if match:
            if current:
                out.append((current, "\n".join(body)))
            current, body = match.group(1), []
        elif line.startswith("#") and current:
            out.append((current, "\n".join(body)))
            current, body = None, []
        elif current:
            body.append(line)
    if current:
        out.append((current, "\n".join(body)))
    return out


def test_the_document_declares_classes_at_all():
    """The vacuity guard. Every assertion below iterates `_blocks()`; an empty one asserts
    nothing and reads green, which is `SG-1` in the file that defines `SG-1`."""
    blocks = _blocks()
    assert len(blocks) >= 8, f"only {len(blocks)} class(es) parsed — the heading form has moved"


def test_every_class_states_the_test_that_catches_the_next_one():
    """§2: *a class with no test is a story*. This is that sentence, carried.

    The test line is what makes an entry worth its space — it says what a reader does
    differently, as against what went wrong once. Without it the file is `0008` §4 again, in a
    shorter font.
    """
    for identifier, body in _blocks():
        assert "*The test:*" in body, (
            f"{identifier} states no test, so it records an incident rather than a class — "
            f"`docs/reference/failure-classes.md` §2")


def test_every_class_says_where_it_was_defined():
    for identifier, body in _blocks():
        assert "*Defined:*" in body, f"{identifier} does not say where it was defined"


def test_class_ids_are_unique_and_in_a_declared_family():
    """The ids are what other files will cite once step 4 migrates citations onto them.

    A duplicate id is worse than a missing class: two citations of `SG-2` would resolve to two
    different rules and nothing would say so — which is `ADR-0009` §0's collision argument, one
    vocabulary over.
    """
    identifiers = [identifier for identifier, _ in _blocks()]
    assert len(identifiers) == len(set(identifiers)), f"duplicate class id in {identifiers}"
    for identifier in identifiers:
        family = identifier.split("-")[0]
        assert family in _FAMILIES, (
            f"{identifier} opens the undeclared family {family!r}; §2 permits a new family, and "
            f"this pin is where it is declared")


def test_the_document_carries_no_number_because_three_are_already_taken_twice():
    """`ADR-0007`/`0007`, `ADR-0008`/`0008`, `ADR-0009`/`0009`. `ADR-0009` §0 refuses a fourth.

    The filename is the claim here: a numbered name under `docs/reference/` would be a fourth
    collision waiting for `docs/audit/0011`.
    """
    assert CLASSES.name == "failure-classes.md"
    assert not re.match(r"^\d", CLASSES.name), "the taxonomy took a number after all"
