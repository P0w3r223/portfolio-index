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
from typing import NamedTuple

_VOID = frozenset({"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
                   "meta", "param", "source", "track", "wbr"})
_SKIPPED = frozenset({"style", "script"})

#: SVG's three paint-alpha presentation attributes. `fill` and `stroke` themselves are *not*
#: here: a colour in an attribute is still the declared colour, and this list is about the
#: page painting something other than what it declared. An alpha is the only one of the three
#: that changes the value between the declaration and the pixel.
#:
#: **Complete for this corpus rather than for SVG.** `style="fill-opacity:.5"` and a
#: gradient stop's `stop-opacity` are two more routes and neither appears on any of the
#: eleven committed surfaces — checked. Stated as the scope it has, because *three places*
#: written as an absolute is the sentence that stops the next reader re-checking.
_PAINT_ALPHA = ("opacity", "fill-opacity", "stroke-opacity")


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


class Element(NamedTuple):
    """One element of the markup, in document order, with a pointer to its parent.

    `nodes` answers *what does the page say*; this answers *what does the page paint, and on
    top of what*. A contrast question needs the second, and it needs an element rather than a
    selector: `.ev-failed` on `auth-log-scan` matches in three places — a legend swatch on
    `--bg`, a mark on a lane, and a mark on a band inside `<g class="row">` — so a check keyed
    on the rule has to pick one ground for all three and is wrong twice. `0008` §3.2 is the
    record of a checker resolving against the nearest card and clearing a change that had to
    be reverted afterwards.

    `parent` indexes back into `Page.elements` and is `-1` for a root, so the ancestors are a
    walk up and the preceding siblings are the lower-indexed entries sharing a parent.
    **The chain means something only where `Page.unclosed` is zero** — the contract
    `tables` ancestry already carries, for the same reason: one element that never closes
    makes every element after it read as its child.

    `attributes` keeps SVG's geometry (`x`, `cx`, `width`) as the strings the markup wrote.
    Parsing them here would put a second reading of the same bytes beside `paint_alphas`,
    which already stores its alpha unparsed for that reason.
    """

    index: int
    tag: str
    classes: frozenset[str]
    attributes: dict[str, str]
    parent: int


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
        #: `(tag, classes, attribute, value)` for every element carrying a paint alpha as a
        #: **presentation attribute** rather than in the stylesheet.
        #:
        #: `clause_1_composited` read CSS `opacity` and `color-mix()` and nothing else, which
        #: made it blind on the one surface that composites per element: `pl-review-sense`
        #: emits `fill-opacity="0.524"` on each confusion-matrix cell, computed from the data,
        #: and draws two text labels over it. The clause whose whole subject is *this page
        #: paints a value that is not the declared one* could not see the page doing exactly
        #: that — and the page's own guard was reading the stylesheet too, where the number is
        #: not. A live SC 1.4.3 failure sat between the two carriers for as long as both
        #: existed.
        #:
        #: Collected here rather than grepped from the markup because an `<svg>` attribute is
        #: structure, and `0007` §2's whole subject is answering a question about the rendered
        #: page from something that is not it.
        self.paint_alphas: list[tuple[str, frozenset[str], str, str]] = []
        #: Every element, in document order, each pointing at its parent. `paint_alphas` is
        #: the same markup read for one attribute and flattened — it carries no ancestry and
        #: no identity, so it can say *this page composites somewhere* and cannot say *this
        #: cell is painted on that rect*. Clause 1's threshold sentence is read per usage
        #: site, and a usage site is an element: `0007` §5 clause 1, `0008` §3.11.
        self.elements: list[Element] = []
        self._open: list[frozenset[str]] = []
        #: Indices into `elements` for the ones still open, pushed and popped in lockstep
        #: with `_open` and `_tags`. A third stack rather than a field on the element,
        #: because `Element` is immutable and a parent is known when the tag opens.
        self._element_stack: list[int] = []
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
        classes = frozenset(attributes.get("class", "").split())
        self.classes.update(classes)

        if tag == "meta":
            self.metas.append(attributes)
        elif tag == "link":
            self.links.append(attributes)
        elif tag == "a" and "href" in attributes:
            self.anchors.append(attributes["href"])
        elif tag == "table":
            ancestors = frozenset().union(*self._open) if self._open else frozenset()
            self.tables.append((classes, ancestors))

        for name in _PAINT_ALPHA:
            if name in attributes:
                self.paint_alphas.append((tag, classes, name, attributes[name]))

        # Before the stack moves, so an element's parent is the one enclosing it and never
        # itself. A void element is recorded and does not open: `<img>` paints and has no
        # children, and pushing it would adopt every element after it.
        self.elements.append(Element(len(self.elements), tag, classes, attributes,
                                     self._element_stack[-1] if self._element_stack else -1))

        if tag not in _VOID:
            self._open.append(classes)
            self._tags.append(tag)
            self._element_stack.append(len(self.elements) - 1)

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
            self._element_stack.pop()
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
            self._element_stack.pop()
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

    def ancestors(self, element: Element) -> list[Element]:
        """`element`'s enclosing elements, nearest first. Empty for a root.

        The *guaranteed* half of a contrast question's ground: containment by an ancestor is
        structural, so it holds whatever the geometry does. A preceding sibling's coverage is
        not, which is why that is a separate call and `0008` §3.11 gives the two different
        weight in a verdict.

        Bounded by the element count rather than by `parent >= 0` alone. A chain cannot be
        longer than the page, so the bound costs nothing and is what makes a broken parent
        pointer redden a test instead of hanging one: setting an element's parent to itself —
        the first mutation this walk is written against — otherwise loops forever appending,
        and took the process to 9.7 GB before it was killed. A guard that cannot be run is not
        a guard.
        """
        chain: list[Element] = []
        parent = element.parent
        for _ in range(len(self.elements)):
            if parent < 0:
                break
            chain.append(self.elements[parent])
            parent = self.elements[parent].parent
        return chain

    def preceding_siblings(self, element: Element) -> list[Element]:
        """The elements opened before `element` under the same parent, in document order.

        Painted before it, and therefore *possibly* under it — possibly, because whether one
        covers the other is geometry and this is structure. The distinction is not academic:
        one `<g class="row">` on `auth-log-scan` holds forty `.ev-failed` circles, so every
        mark but the first has thirty-nine of these, each already its own colour. A rule
        treating every preceding sibling as a ground the element must clear reports all one
        hundred and thirty-nine marks on that page as undecidable — measured, and the reason
        this returns the candidates rather than a verdict about them.
        """
        return [other for other in self.elements[:element.index]
                if other.parent == element.parent]

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
