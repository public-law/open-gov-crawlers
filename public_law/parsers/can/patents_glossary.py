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
        Subject(LoCSubject("sh85098655"), String("Patents")),
        Subject(WikidataTopic("Q3039731"), String("Patent Law")),
    )

    return Metadata(
        dcterms_title=String("Canadian Patent Glossary"),
        dcterms_language="en",
        dcterms_coverage="CAN",
        # Info about original source
        dcterms_source=source_url,
        publiclaw_sourceModified="unknown",
        publiclaw_sourceCreator=String(
            "Canadian Intellectual Property Office"),
        dcterms_subject=subjects,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """Parse the glossary entries from the HTML response.

    The entries are in definition lists (<dl>), with each <dt> containing the phrase
    and each <dd> containing the definition.
    """
    entries: list[GlossaryEntry] = []
    soup = make_soup(html)

    # Find all definition lists
    dls = soup.find_all("dl")
    if not dls:
        return tuple()

    for dl in dls:
        # Each dl contains dt/dd pairs
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")

        # Ensure we have matching pairs
        if len(dts) != len(dds):
            continue

        for dt, dd in zip(dts, dds):
            # Get the phrase from the dt, handling both text and strong tags
            phrase_elem = dt.find("strong") or dt
            phrase = phrase_elem.get_text(strip=True)
            if phrase == "Date modified:":
                continue

            # Get the definition from the dd
            definition = dd.get_text(strip=True)

            if phrase and definition:
                entries.append(
                    GlossaryEntry(
                        phrase=String(phrase),
                        definition=Sentence(
                            ensure_ends_with_period(definition)),
                    )
                )

    return tuple(entries)
