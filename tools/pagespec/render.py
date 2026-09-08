"""What a reader meets on the page, parsed from its markup.

The core is `apply-scout/tests/test_docs_page.py`'s `_Rendered`, which had the hard parts
solved: a `_VOID` set so elements HTML never closes do not stay on the open stack forever,
and an `unclosed` count so a wrapper that never closes cannot make every table below it read
as wrapped. That is a false green in the direction that matters, and this keeps the guard.

Widened for the spec: `<title>`, `<link>`, anchors, and the class of every element, because
clauses 2, 4, 5, 6 and 7 each ask about a different part of the head or the shell.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

_VOID = frozenset({"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
                   "meta", "param", "source", "track", "wbr"})
_SKIPPED = frozenset({"style", "script"})


_ASCII_WHITESPACE = re.compile("[ \t\r\n\f\v]+")


def flatten(text: str) -> str:
    """Collapse runs of *ASCII* whitespace only.

    `str.split()` splits on Unicode whitespace, and `' '.isspace()` and
    `' '.isspace()` are both **True** — so the obvious one-liner silently rewrites the
    narrow no-break space and the no-break space into ordinary spaces. Clause 8 counts
    exactly those two codepoints, so the obvious version would make every page look like it
    separates thousands with a plain space. Three earlier tallies of this were wrong; this
    would have been the fourth.
    """
    return _ASCII_WHITESPACE.sub(" ", text).strip()


class Page(HTMLParser):
    """One published page, read once.

    Attributes are collected here where `_Rendered` deliberately dropped them, because the
    spec asks about `<meta>` names, `<link>` hrefs and class names — all attributes, none of
    them text a reader sees. The text/markup separation that mattered to `apply-scout` is
    kept in `nodes`, which still excludes `<style>` and `<script>`.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.headline = ""
        #: One entry per text node: the text, and the tag names enclosing it, outermost
        #: first. The ancestry is what clause 8's census reads — `doc-extract` prints
        #: `3<U+00A0>466,62` inside `<code>` as a *displayed specimen* of a foreign format,
        #: and it is **the only grouped figure inside `<code>` on the twelve**. Flattened to
        #: a list of strings, the specimen and a body figure are the same node and `0008`
        #: S9c's exemption could only be written as a literal-string carve-out — the
        #: "silently widen" failure §4.11 forbids of exactly this exemption.
        #:
        #: *This said "every other grouped figure sits in `<p>`, `<td>` or SVG `<text>`",
        #: which the census in the same commit refutes — fourteen counterexamples. It was
        #: then rewritten as the distribution spelled out, which is a hand-typed figure in a
        #: docstring and goes stale in silence: `0009` §8 row 1 is the record refusing to
        #: type a census for exactly that reason. **The distribution is what the census
        #: prints on every run**; the only fact the exemption needs is uniqueness of
        #: `<code>`, and that is the one sentence left here.*
        self.nodes: list[tuple[str, tuple[str, ...]]] = []
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.anchors: list[str] = []
        self.inline_styles: list[str] = []
        self.classes: set[str] = set()
        #: (own classes, ancestor classes) per <table>. The table's own classes matter
        #: because `wroclaw-air-insights` makes the table itself the scroller under
        #: `max-width: 640px` — a fourth mechanism, and the one that broke `measure_page.py`.
        self.tables: list[tuple[frozenset[str], frozenset[str]]] = []
        self._open: list[frozenset[str]] = []
        #: The same stack as `_open`, holding tag names instead of classes, and it is pushed
        #: and popped in lockstep with it. Two stacks rather than one stack of pairs because
        #: `handle_starttag` unions `_open` to build a table's ancestry, and a stack of pairs
        #: would put a tag name into a set of class names.
        self._tags: list[str] = []
        self._skipped = 0
        self._style: list[str] | None = None
        self._title: list[str] | None = None
        self._in_svg = 0
        self._heading: list[str] | None = None

    # -- structure -------------------------------------------------------------------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: (value or "") for name, value in attrs}
        self.classes.update(attributes.get("class", "").split())

        if tag == "meta":
            self.metas.append(attributes)
        elif tag == "link":
            self.links.append(attributes)
        elif tag == "a" and "href" in attributes:
            self.anchors.append(attributes["href"])
        elif tag == "table":
            ancestors = frozenset().union(*self._open) if self._open else frozenset()
            self.tables.append((frozenset(attributes.get("class", "").split()), ancestors))

        if tag not in _VOID:
            self._open.append(frozenset(attributes.get("class", "").split()))
            self._tags.append(tag)

        if tag in _SKIPPED:
            self._skipped += 1
            if tag == "style":
                self._style = []
        elif tag == "svg":
            self._in_svg += 1
        elif tag == "title" and not self._in_svg and not self.title:
            # SVG carries its own <title> for accessibility. Taking the last one seen makes
            # the document title read as the name of the final chart on the page.
            self._title = []
        elif tag == "h1":
            self._heading = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """`<link/>` and friends, which never reach `handle_endtag`.

        Every counter `handle_starttag` raises has to come back down here, not just the
        open-element stack. An XHTML-style `<script src="x.js" />` would otherwise leave
        `_skipped` at one for the rest of the parse, and **every later text node would be
        dropped in silence** — clause 8 would report no grouped figure on a page full of
        them, with no error to notice.
        """
        self.handle_starttag(tag, attrs)
        if tag not in _VOID and self._open:
            self._open.pop()
            self._tags.pop()
        if tag in _SKIPPED:
            self._skipped = max(self._skipped - 1, 0)
            if tag == "style":
                self._style = None
        elif tag == "svg":
            self._in_svg = max(self._in_svg - 1, 0)
        # **Two of the sinks this docstring names did not come back down** — and the first
        # repair lowered them for *every* self-closed tag, which is far worse than the hole it
        # closed: `<h1>Fast <br/> answers</h1>` cleared the heading collector, so
        # `clause_4_opening` reported `4 h1 FAIL — no <h1>` on a page that has one, and
        # `"4 h1"` gates. `<br/>`, `<img/>` and `<wbr/>` inside a heading are ordinary markup;
        # `<h1/>` is not. Scoped to the tag that opened the collector, the way `handle_endtag`
        # already does it.
        elif tag == "title" and self._title is not None:
            self._title = None
        elif tag == "h1" and self._heading is not None:
            self._heading = None

    def handle_endtag(self, tag: str) -> None:
        if tag not in _VOID and self._open:
            self._open.pop()
            self._tags.pop()
        if tag in _SKIPPED:
            self._skipped = max(self._skipped - 1, 0)
            if tag == "style" and self._style is not None:
                self.inline_styles.append("".join(self._style))
                self._style = None
        elif tag == "svg":
            self._in_svg = max(self._in_svg - 1, 0)
        elif tag == "title" and self._title is not None:
            self.title = flatten("".join(self._title))
            self._title = None
        elif tag == "h1" and self._heading is not None:
            if not self.headline:
                self.headline = flatten("".join(self._heading))
            self._heading = None

    def handle_data(self, data: str) -> None:
        if self._style is not None:
            self._style.append(data)
        if self._skipped:
            return
        self.nodes.append((data, tuple(self._tags)))
        for sink in (self._title, self._heading):
            if sink is not None:
                sink.append(data)

    # -- what the clauses ask ---------------------------------------------------------

    @property
    def unclosed(self) -> int:
        """Elements still open at end of parse. Any number but zero voids the ancestry.

        `apply-scout`'s note applies unchanged: this counts every non-void tag as needing an
        explicit close, which HTML5 does not require. Markup that legally omits `</li>` would
        be reported here. That fails closed, which is the right direction.
        """
        return len(self._open)

    @property
    def text_nodes(self) -> list[tuple[str, tuple[str, ...]]]:
        """Each text node that carries something, flattened, with the tags enclosing it.

        The one place a text node is flattened and the one place an empty one is dropped.
        `rendered_text` is this joined, and `clauses.grouped_figures` reads it directly for
        the ancestry the join destroys — so the census and the clause cannot disagree about
        what the page says, only about what to do with it.
        """
        carrying = ((flatten(text), ancestry) for text, ancestry in self.nodes)
        return [(text, ancestry) for text, ancestry in carrying if text]

    @property
    def rendered_text(self) -> str:
        """The page's text, with a hard break between adjacent text nodes.

        Concatenating nodes directly welds the last number of one element to the first of the
        next: `auth-log-scan`'s stat tiles print `5` and `315` side by side and read as the
        grouped figure `5 315`, which that page does not contain. This is the mechanism behind
        every wrong separator tally in the record, and the break is what forbids it — a grouped
        figure lives inside one text node or it is not one figure.
        """
        return chr(10).join(text for text, _ in self.text_nodes)

    def meta(self, key: str) -> str | None:
        """The content of `<meta name=key>` or `<meta property=key>`, whichever exists."""
        for entry in self.metas:
            if entry.get("name") == key or entry.get("property") == key:
                return entry.get("content", "")
        return None

    def stylesheet_hrefs(self) -> list[str]:
        return [link["href"] for link in self.links
                if "stylesheet" in link.get("rel", "").lower() and link.get("href")]


def parse(html: str) -> Page:
    page = Page()
    page.feed(html)
    page.close()
    return page
