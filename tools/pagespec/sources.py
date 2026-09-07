"""Where each published surface's bytes come from — the I/O boundary, and nothing else.

Eleven repositories publishing twelve surfaces, **three different kinds of source**, and
getting this wrong is the failure `0007` §2 calls the one every earlier attempt made:
answering a question about the rendered page from something that is not the rendered page.

- Ten commit a `docs/index.html`. Read the file — and under `--fetch`, read what is
  actually served and compare the two. *This line asserted the identity as fact until
  `0009` §3.1 named it as C1: nothing measured it, and `0008` §6 carried it as a
  manual row. The `served` finding is what measures it now.*
- `car-price-ml` commits a **second** surface, `docs/app/index.html` — hand-written inside a
  repository that generates and byte-diffs everything else.
- `wroclaw-air-insights` commits **no HTML at all** (`.gitignore:25`). Its page is a Pages
  artifact rebuilt daily, so it exists only at the live URL. Reading `reports/site/` gets an
  untracked local build that has been 24 days stale and produced a wrong answer that survived
  a session.
- `token-budget` has no page. It is the twelfth repository, is not a surface, and is not
  checked — which is why the repository count here is eleven and not twelve.
"""

from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from . import render

#: Why a sheet was not read, when the reason is *by design*. Declared here, beside the only
#: code that writes it, and imported by the readers — `0008` §5 carries "the marker is prose
#: built in one module and matched in two others" as a residual, and this is that closed.
THIRD_PARTY = "third party, not read"

USER_AGENT = "pagespec (portfolio conformance checker)"

FETCH_TIMEOUT = 30


def describe(entry: tuple[str, str]) -> str:
    """One unreadable sheet, as a line. The pair is the value; this is the only rendering.

    `clauses` and `__main__` each built this string independently for one revision. Nothing
    parsed either, so the divergence was harmless — but the two are printed under different
    gate headers about the same fact, and a reader comparing them is entitled to one wording.
    """
    href, why = entry
    return f"{href} ({why})"


@dataclass(frozen=True)
class Surface:
    """One published page: what to call it, and where its bytes are."""

    name: str
    repo: str
    path: str | None = None
    url: str | None = None
    note: str = ""

    @property
    def must_fetch(self) -> bool:
        return self.path is None

    @property
    def published(self) -> str:
        """Where this surface is actually served. Every surface has one; only one lacks a file."""
        return self.url or _published(self.repo, self.path)


#: Where the pages are served from. A project site, so each repository is a path segment.
PAGES = "https://p0w3r223.github.io/"


def _published(repo: str, path: str | None) -> str:
    """The URL a committed page is served at, derived rather than typed twelve times.

    GitHub Pages serves `docs/` as the site root and `index.html` as a directory, so
    `docs/app/index.html` in `car-price-ml` is `/car-price-ml/app/`. Derived because a typed
    table is a second registry of the same fact — `0009` N1's shape, and this file already
    carries one pair of those.
    """
    if path is None:
        raise ValueError("a surface with no committed path must state its url")
    inner = path.removeprefix("docs/").removesuffix("index.html").strip("/")
    return f"{PAGES}{repo}/" + (f"{inner}/" if inner else "")


SURFACES: tuple[Surface, ...] = (
    Surface("ab-lab", "ab-lab", "docs/index.html"),
    Surface("apply-scout", "apply-scout", "docs/index.html"),
    Surface("auth-log-scan", "auth-log-scan", "docs/index.html"),
    Surface("car-price-ml", "car-price-ml", "docs/index.html"),
    Surface("car-price-ml/app", "car-price-ml", "docs/app/index.html",
            note="hand-written; the only surface here CI does not byte-diff"),
    Surface("doc-extract", "doc-extract", "docs/index.html"),
    Surface("it-job-radar", "it-job-radar", "docs/index.html"),
    Surface("mini-traceroute", "mini-traceroute", "docs/index.html",
            note="the one page whose CSS is not inlined"),
    Surface("mlops-car-price", "mlops-car-price", "docs/index.html"),
    Surface("pl-jobs-lora", "pl-jobs-lora", "docs/index.html"),
    Surface("pl-review-sense", "pl-review-sense", "docs/index.html"),
    Surface("wroclaw-air-insights", "wroclaw-air-insights",
            url=PAGES + "wroclaw-air-insights/",
            note="commits no HTML; live URL is the only surface that exists"),
)


@dataclass
class Loaded:
    """A surface's markup and its complete stylesheet, with what could not be read."""

    surface: Surface
    html: str
    css: str
    stylesheets: list[str] = field(default_factory=list)
    #: `(href, why)` and not prose. Three readers have now had to recover the href from a
    #: formatted string: the first split on ", " and the third-party marker contains that
    #: separator; the second split on " (" and a later change put an em dash before it. The
    #: structured value was available at every one of those sites, and `_unread_same_origin`
    #: had already written that sentence down before the third reader was added.
    unreadable: list[tuple[str, str]] = field(default_factory=list)
    #: What the wire returned, when the run read it. **Bytes, not text**: `_fetch` decodes with
    #: `errors="replace"`, which collapses two *different* invalid bytes to one U+FFFD, so a
    #: hash taken after decoding cannot tell those apart. The comparison has to happen where
    #: the bytes still exist.
    served: bytes | None = None
    #: What the committed file holds. `None` for the surface that commits no HTML.
    committed: bytes | None = None
    #: Why the fetch did not happen, when one was attempted and failed.
    served_error: str | None = None
    #: Same-origin sheets the wire could not deliver. A separate list rather than a marker
    #: inside `unreadable`, because the two get opposite policies and `0008` §5 carries what
    #: it costs to encode a policy as prose one module builds and another matches. A missing
    #: *file* is the page's business and gates; a *network* failure is not and does not — the
    #: same distinction `served` already makes between a 404 and a DNS blip, and the argument
    #: `_local_sheet` makes on the file path: a false gate is worse than a missing one.
    #:
    #: Unreachable before `--fetch` read the eleven. Every scheduled run now fetches their
    #: sheets, so `mini-traceroute` and `car-price-ml/app` would have gated on any blip.
    unreachable: list[tuple[str, str]] = field(default_factory=list)
    #: The page answered 404 or 410. A regression, not a wire failure, and the two must not
    #: arrive as the same line — `0007` §2's whole subject is answering a question about a
    #: page from something that is not that page, and "gone" is an answer.
    served_gone: bool = False


def _fetch(url: str) -> bytes:
    """The served bytes, undecoded.

    It returned `str` until the served-versus-committed comparison existed. Decoding first
    with `errors="replace"` maps every invalid byte to the same U+FFFD, so two pages differing
    only in an undecodable byte would hash identically and the comparison would report them
    equal — a false `PASS` on the one question this function now exists to answer.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
        return response.read()


def load(surface: Surface, root: Path, *, allow_fetch: bool,
         errors: dict[str, str] | None = None) -> Loaded | None:
    """The surface's markup, or `None` when it cannot be read.

    **Under `--fetch` the clauses are answered from the served bytes, not from the file.**
    That is `0009` §3.1's finding C1: this checker answers a question about a *published* page
    by reading a *committed* one, and CI reads that file at the superproject's pinned gitlink —
    so a page could regress in a public repository and stay invisible here until somebody
    bumped a pointer. The fallback order is served, then committed, then nothing, and the
    `served` finding says which of the three happened.

    Returning `None` rather than an empty page matters: an empty page satisfies no clause and
    would be reported as thirteen failures, which reads as a portfolio-wide regression when
    the truth is that the network was off.
    """
    committed: bytes | None = None
    page_path = root / surface.repo / surface.path if surface.path else None
    if page_path is not None and page_path.is_file():
        committed = page_path.read_bytes()

    served: bytes | None = None
    served_error: str | None = None
    served_gone = False
    if allow_fetch:
        try:
            served = _fetch(surface.published)
        except Exception as error:
            # The exception text, not just the fact. A 404 (the page is gone, a real
            # regression) and a DNS blip are the same line without it, and since `0008`
            # S-gate the scheduled job gates. Recorded on the surface rather than raised,
            # because a page that cannot be read must not stop the other eleven.
            served_error = f"{type(error).__name__}: {error}"
            served_gone = getattr(error, "code", None) in (404, 410)
            if errors is not None:
                errors[surface.name] = served_error

    if served is None and surface.must_fetch:
        # The one surface with no file to fall back to. This branch is why a failed fetch
        # still ends the run for it, and `test_a_failed_fetch_is_not_reported_as_a_flag_the
        # _reader_forgot` is the guard on that.
        return None
    if served is None and committed is None:
        return None

    source = served if served is not None else committed
    # `errors="replace"` on both branches: one undecodable byte in one page must not end the
    # run for the other eleven. The undecoded bytes are kept on `Loaded` for the comparison.
    html = source.decode("utf-8", errors="replace")
    loaded = (_with_styles(surface, html, base_url=surface.published) if served is not None
              else _with_styles(surface, html, base_path=page_path))
    loaded.served = served
    loaded.committed = committed
    loaded.served_error = served_error
    loaded.served_gone = served_gone
    return loaded


def _local_sheet(base_path: Path, href: str) -> Path:
    """The file a same-origin href names, resolved as a URL reference the way the fetch
    branch resolves it — plus one fallback the wire does not have.

    An href is a URL reference and not a path: the query string is not part of it, and
    `%20` means a space. `urljoin` has always done both for the fetched surface; this branch
    joined the raw string, so `styles.css?v=2` reported a file sitting right there as
    unreadable — and an unread same-origin sheet **refuses the build**.

    **The literal name is tried second, and that is an asymmetry rather than parity.**
    `urljoin` sends `%20` to the server, which decodes it, so a file genuinely called
    `my%20x.css` on the origin would 404 on the wire and is read here. Decoding is right
    by the spec,
    but a file genuinely called `my%20x.css` would then be reported unreadable, and this
    function's whole subject is that a false gate is worse than a missing one. Reading either
    candidate answers the question the clauses are about to ask; refusing a page over which
    of two spellings is on disk answers nothing.
    """
    without_query = urllib.parse.urlparse(href).path
    decoded = base_path.parent / urllib.parse.unquote(without_query)
    if decoded.is_file():
        return decoded
    literal = base_path.parent / without_query
    return literal if literal.is_file() else decoded


def _with_styles(surface: Surface, html: str, *, base_path: Path | None = None,
                 base_url: str | None = None) -> Loaded:
    """Inline `<style>` blocks plus every same-origin `<link>`ed sheet, concatenated.

    Reading only the inline blocks is the trap that recorded `mini-traceroute` as having no
    `overflow-x` rule across three sessions, so the external sheets are not optional and a
    sheet that cannot be read is reported rather than skipped.
    """
    page = render.parse(html)
    parts = list(page.inline_styles)
    names: list[str] = ["<style>"] * len(page.inline_styles)
    unreadable: list[tuple[str, str]] = []
    unreachable: list[tuple[str, str]] = []

    for href in page.stylesheet_hrefs():
        if href.startswith(("http://", "https://", "//")):
            unreadable.append((href, THIRD_PARTY))
            continue
        try:
            if base_path is not None:
                # The href is a URL reference, not a path. `styles.css?v=2` named a file that
                # exists on disk and was reported unreadable — and since `0008` S-gate an
                # unread same-origin sheet *gates*, so that was CI refusing a page that is
                # fine, under a message pointing at a stylesheet the reader can open. The
                # fetch branch below has always been right about this, through `urljoin`.
                #
                # A root-relative href stays unreadable, and deliberately: `/assets/x.css` on a
                # GitHub Pages *project* site resolves under the site root and not under the
                # repository, so there is no file here to read and saying so is correct.
                parts.append(_local_sheet(base_path, href).read_text(
                    encoding="utf-8", errors="replace"))
            else:
                # `_fetch` returns bytes since the served-versus-committed comparison
                # exists; a stylesheet is text to every reader downstream, so it is
                # decoded here rather than making the seam return two types.
                parts.append(_fetch(urllib.parse.urljoin(base_url, href))
                             .decode("utf-8", errors="replace"))
            names.append(href)
        except Exception as error:
            # The cause, not just the fact — the same argument the fetch path above already
            # makes, on a path that now gates daily. A rename, a permission error and a
            # missing file arrive as one identical line without it, and `0008` §5 has carried
            # this as a residual since the S-gate review.
            # `strerror` where the exception carries one: the href already names the file,
            # and `str(error)` repeats it as an absolute machine path into the gate output.
            why = getattr(error, "strerror", None) or str(error)
            described = (href, f"{type(error).__name__}: {why}")
            # A wire failure on the fetch path is the network, not the page. An HTTP
            # status is the page answering, so that keeps gating: a 404 on a stylesheet
            # is a real defect and a DNS blip is not.
            if base_url is not None and not isinstance(error, urllib.error.HTTPError):
                unreachable.append(described)
            else:
                unreadable.append(described)

    return Loaded(surface, html, "\n".join(parts), names, unreadable,
                  unreachable=unreachable)
