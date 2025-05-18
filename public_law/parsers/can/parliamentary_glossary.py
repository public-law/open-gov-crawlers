from typing import Any, Iterable, List, cast

from bs4 import Tag, ResultSet
from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from public_law import text

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, WikidataTopic
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    """
    The top-level, public function of this module. It performs the
    complete parse of the HTTP response.
    """
    metadata = _make_metadata(html)
    entries = _parse_entries(html)

    return GlossaryParseResult(metadata, entries)


def _make_metadata(html: HtmlResponse) -> Metadata:
    source_url = URL(html.url)
    subjects = (
        Subject(LoCSubject("sh85075807"), String("Legislative bodies")),
        Subject(WikidataTopic("Q35749"), String("Parliament")),
    )

    return Metadata(
        dcterms_title=String(
            "Glossary of Parliamentary Terms for Intermediate Students"),
        dcterms_language="en",
        dcterms_coverage="CAN",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified="unknown",
        publiclaw_sourceCreator=String("Parliament of Canada"),
        dcterms_subject=subjects,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse the glossary entries from the HTML response.
    The entries are in a <dl> inside .glossary-terms-intermediate, with <dt> for terms and <dd> for definitions.
    Robustly pair each <dt> with the next <dd>, skipping non-term elements and handling malformed HTML.
    """
    entries: list[GlossaryEntry] = []
    soup = make_soup(html)
    container = soup.find("div", class_="glossary-terms-intermediate")
    if not container or not isinstance(container, Tag):
        return tuple()
    dl = container.find("dl")
    if not dl or not isinstance(dl, Tag):
        return tuple()
    children = list(dl.children)
    i = 0
    while i < len(children):
        dt = children[i]
        if isinstance(dt, Tag) and dt.name == "dt":
            # Find the next <dd>
            j = i + 1
            while j < len(children):
                dd = children[j]
                if isinstance(dd, Tag) and dd.name == "dd":
                    phrase = dt.get_text(strip=True)
                    definition = dd.get_text(strip=True)
                    if phrase and definition:
                        entries.append(
                            GlossaryEntry(
                                phrase=String(phrase),
                                definition=Sentence(
                                    ensure_ends_with_period(definition))
                            )
                        )
                    break
                j += 1
            i = j
        i += 1
    entries.sort(key=lambda e: e.phrase.lower())
    return tuple(entries)
