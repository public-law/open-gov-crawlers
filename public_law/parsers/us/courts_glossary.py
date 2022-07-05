from scrapy.http.response.html import HtmlResponse

from ...text import NonemptyString as NS, make_soup, normalize_whitespace
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    # pyright: reportUnknownMemberType=false
    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=NS("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage=NS("USA"),
            # Info about original source
            dcterms_source=NS("https://www.uscourts.gov/glossary"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=NS("United States Courts"),
        ),
        entries=__parse_entries(html),
    )


def __parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry]:
    soup = make_soup(html)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=NS(normalize_whitespace(phrase.text)),
            definition=NS(normalize_whitespace(defn.text)),
        )
        for phrase, defn in raw_entries
    )
