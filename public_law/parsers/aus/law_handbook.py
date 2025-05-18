from typing import Any, List, Optional

from bs4 import Tag
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
        Subject(LoCSubject("sh85075119"), String("Law")),
        Subject(WikidataTopic("Q7748"), String("Law")),
    )

    return Metadata(
        dcterms_title=String("Law Handbook Glossary"),
        dcterms_language="en",
        dcterms_coverage="AUS",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified="unknown",
        publiclaw_sourceCreator=String(
            "Legal Services Commission of South Australia"),
        dcterms_subject=subjects,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse the glossary entries from the HTML response.

    The entries are in a definition list (<dl>) with <dt> containing <span class="glossterm"> for terms 
    and <dd class="glossdef"> containing <p> for definitions.
    """
    entries: list[GlossaryEntry] = []
    soup = make_soup(html)

    # Find all dt/dd pairs in the glossary
    for dt, dd in zip(soup.find_all("dt"), soup.find_all("dd", class_="glossdef")):
        # Extract the text content from the span.glossterm element
        phrase_elem = dt.find("span", class_="glossterm")
        if not phrase_elem:
            continue

        phrase = phrase_elem.get_text().strip()
        definition = dd.find("p").get_text().strip()

        if phrase and definition:
            entries.append(
                GlossaryEntry(
                    phrase=String(phrase),
                    definition=Sentence(ensure_ends_with_period(definition)),
                )
            )

    # Do not sort; preserve source order
    return tuple(entries)
