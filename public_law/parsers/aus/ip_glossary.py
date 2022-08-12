from datetime import date, datetime
from typing import Iterable
from scrapy.http.response.html import HtmlResponse
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import URL, LoCSubject, NonemptyString as String
from ...metadata import Metadata, Subject


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    entries = _parse_entries(html)
    mod_date = _parse_mod_date(html)

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("IP Glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            # Info about original source
            dcterms_source=String(html.url),  # type: ignore
            publiclaw_sourceModified=mod_date,
            publiclaw_sourceCreator=String("IP Australia"),
            publiclaw_readingEase=reading_ease(entries),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85071120"),  # type: ignore
                    rdfs_label=String("Justice, Administration of"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q16514399"),
                    rdfs_label=String("Administration of justice"),
                ),
            ),
        ),
        entries=entries,
    )


def _parse_mod_date(html: HtmlResponse) -> date:
    """
    Parse the modification date from HTML like this:

    <span class="date-display-single" property="dc:date" datatype="xsd:dateTime" content="2021-03-26T00:00:00+11:00">26 March 2021</span>
    """
    mod_date_str: str = (
        html.selector.css("span.date-display-single").xpath("@content").get()  # type: ignore
    )
    return datetime.fromisoformat(mod_date_str).date()


def _parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    return []
