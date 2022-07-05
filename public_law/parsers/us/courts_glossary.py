# SOURCE_URL = 'https://www.uscourts.gov/glossary'
# HTML_TITLE = response.xpath('//title/text()').get()

from typing import cast
from bs4 import BeautifulSoup
from scrapy.http.response.html import HtmlResponse

from ...text import NonemptyString as NS
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


def __parse_entries(html: HtmlResponse) -> list[GlossaryEntry]:
    soup = BeautifulSoup(cast(str, html.body), "html.parser")
    raw_entries = zip(soup("dt"), soup("dd"))

    return [
        GlossaryEntry(
            phrase=NS(phrase.text),
            definition=NS(defn.text),
        )
        for phrase, defn in raw_entries
    ]
