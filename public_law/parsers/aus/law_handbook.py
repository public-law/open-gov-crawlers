from typing import List

from scrapy.http.response.html import HtmlResponse

from public_law.html import TypedSoup, parse_html

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    """
    The top-level, public function of this module. It performs the
    complete parse of the HTTP response.
    """
    metadata = _make_metadata(html)
    entries = _parse_entries(html)

    return GlossaryParseResult(metadata, entries)


def _make_metadata(html: HtmlResponse) -> Metadata:
    """
    This Glossary defies the planned subject tagging scheme
    because it has terms from a wide variety of areas of law.

    TODO: Figure out a way to appropriately choose subjects
    for it.
    """
    source_url = URL(html.url)
    subjects = (
        Subject(
            uri=LoCSubject("sh85075720"),
            rdfs_label=String("Legal aid"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q707748"),
            rdfs_label=String("Legal aid"),
        ),
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
    entries: List[GlossaryEntry] = []
    soup = parse_html(html)

    # Find all dt/dd pairs in the glossary
    dts = soup.find_all("dt")
    dds = soup.find_all("dd", class_="glossdef")

    for dt, dd in zip(dts, dds):
        # Extract the text content from the span.glossterm element
        phrase_elem = dt.find("span", class_="glossterm")
        if not phrase_elem:
            continue

        phrase = phrase_elem.get_text(strip=True)

        # Find the definition paragraph
        p_elem = dd.find("p")
        if not p_elem:
            continue

        definition = p_elem.get_text(strip=True)

        if phrase and definition:
            entries.append(
                GlossaryEntry(
                    phrase=String(phrase),
                    definition=Sentence(ensure_ends_with_period(definition)),
                )
            )

    # Do not sort; preserve source order
    return tuple(entries)
