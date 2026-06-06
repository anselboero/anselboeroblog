"""Extract attributed quotes from an Entry's markdown body.

A quote is a markdown blockquote whose attribution line is a link to a person
page, e.g.:

    > Real artists ship.
    >
    > — [Steve Jobs](/people/steve-jobs/)

The slug is read from the ``/people/<slug>/`` link. Blockquotes without such a
link are left alone (treated as ordinary blockquotes, not quotes).
"""
import re

# A markdown link pointing at a person detail page: [Name](/people/<slug>/)
# The host part is optional so absolute URLs work too.
PERSON_LINK_RE = re.compile(
    r'\[[^\]]*\]\((?:https?://[^/]+)?/people/(?P<slug>[\w-]+)/?\)'
)

# Any markdown link: [text](url)
LINK_RE = re.compile(r'\[[^\]]*\]\((?P<url>[^)]+)\)')


def _source_url(attribution_line):
    """Return the first non-person link URL on the attribution line, or ''."""
    for match in LINK_RE.finditer(attribution_line):
        url = match.group('url').strip()
        if not PERSON_LINK_RE.match(match.group(0)):
            return url
    return ''


def _iter_blockquotes(body):
    """Yield the inner text of each top-level blockquote block in ``body``."""
    lines = body.splitlines()
    block = None
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('>'):
            # Drop the leading '>' and a single optional space.
            content = stripped[1:]
            if content.startswith(' '):
                content = content[1:]
            if block is None:
                block = []
            block.append(content)
        else:
            if block is not None:
                yield '\n'.join(block)
                block = None
    if block is not None:
        yield '\n'.join(block)


def extract_quotes(body):
    """Return ``[{'text', 'slug', 'order'}, ...]`` for attributed blockquotes.

    Quotes are returned in document order. A blockquote with no person link is
    skipped. The attribution line itself is stripped from the quote text.
    """
    quotes = []
    for block in _iter_blockquotes(body):
        match = PERSON_LINK_RE.search(block)
        if not match:
            continue
        slug = match.group('slug')
        block_lines = block.splitlines()
        # The attribution line carries the person link; any other link on it is
        # the external source. Every other line is the quote text.
        attribution = next(ln for ln in block_lines if PERSON_LINK_RE.search(ln))
        text_lines = [ln for ln in block_lines if not PERSON_LINK_RE.search(ln)]
        text = '\n'.join(text_lines).strip()
        if not text:
            continue
        quotes.append({
            'text': text,
            'slug': slug,
            'source_url': _source_url(attribution),
            'order': len(quotes),
        })
    return quotes
