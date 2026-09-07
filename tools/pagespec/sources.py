"""Where each published surface's bytes come from — the I/O boundary, and nothing else.

Eleven repositories publishing twelve surfaces, **three different kinds of source**, and
getting this wrong is the failure `0007` §2 calls the one every earlier attempt made:
answering a question about the rendered page from something that is not the rendered page.

- Ten commit a `docs/index.html` served byte-identically. Read the file.
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
            url="https://p0w3r223.github.io/wroclaw-air-insights/",
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


def _fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
        return response.read().decode("utf-8", errors="replace")


def load(surface: Surface, root: Path, *, allow_fetch: bool,
         errors: dict[str, str] | None = None) -> Loaded | None:
    """The surface's markup, or `None` when it cannot be read.

    Returning `None` rather than an empty page matters: an empty page satisfies no clause and
    would be reported as thirteen failures, which reads as a portfolio-wide regression when
    the truth is that the network was off.
    """
    if surface.must_fetch:
        if not allow_fetch:
            return None
        try:
            html = _fetch(surface.url)
        except Exception as error:
            # The exception text, not just the fact. Since `0008` S-gate the scheduled job
            # is the only reader of this surface and it now gates, so `fetch failed` is a
            # thing somebody has to act on — and a 404 (the page is gone, a real regression)
            # and a DNS blip are the same line without this. Recorded on the surface rather
            # than raised, because a page that cannot be read must not stop the other eleven
            # from being reported.
            if errors is not None:
                errors[surface.name] = f"{type(error).__name__}: {error}"
            return None
        return _with_styles(surface, html, base_url=surface.url)

    page_path = root / surface.repo / surface.path
    if not page_path.is_file():
        return None
    # `errors="replace"`, matching the fetch path above: one undecodable byte in one
    # page must not end the run for the other eleven.
    html = page_path.read_text(encoding="utf-8", errors="replace")
    return _with_styles(surface, html, base_path=page_path)


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
                parts.append(_fetch(urllib.parse.urljoin(base_url, href)))
            names.append(href)
        except Exception as error:
            # The cause, not just the fact — the same argument the fetch path above already
            # makes, on a path that now gates daily. A rename, a permission error and a
            # missing file arrive as one identical line without it, and `0008` §5 has carried
            # this as a residual since the S-gate review.
            # `strerror` where the exception carries one: the href already names the file,
            # and `str(error)` repeats it as an absolute machine path into the gate output.
            why = getattr(error, "strerror", None) or str(error)
            unreadable.append((href, f"{type(error).__name__}: {why}"))

    return Loaded(surface, html, "\n".join(parts), names, unreadable)
