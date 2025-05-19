from typing import Any, List, cast

from bs4 import Tag, ResultSet
from scrapy.http.response.html import HtmlResponse

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
        Subject(LoCSubject("sh85034086"), String("Criminal Procedure")),
        Subject(WikidataTopic("Q146071"), String("Criminal Procedure")),
    )

    return Metadata(
        dcterms_title=String("US Courts Glossary"),
        dcterms_language="en",
        dcterms_coverage="USA",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified="unknown",
        publiclaw_sourceCreator=String("San Diego Superior Court"),
        dcterms_subject=subjects,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse the glossary entries from the HTML response.

    The entries are in a table, with each <tr> containing two <td>s: the first is the phrase, the second is the definition.
    """
    entries: list[GlossaryEntry] = []
    soup = make_soup(html)
    table = soup.find("table")
    if not table or not isinstance(table, Tag):
        return tuple()

    rows: ResultSet[Tag] = table.find_all("tr")
    for row in rows:
        cells: ResultSet[Tag] = row.find_all("td")
        if len(cells) < 2:
            continue
        phrase = cells[0].get_text(strip=True)
        definition = cells[1].get_text(strip=True)
        if phrase and definition:
            entries.append(
                GlossaryEntry(
                    phrase=String(phrase),
                    definition=Sentence(ensure_ends_with_period(definition)),
                )
            )
    return tuple(entries)
