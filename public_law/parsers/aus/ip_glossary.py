from datetime import date, datetime
from typing import cast

from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    entries = _parse_entries(html)
    mod_date = _parse_mod_date(html)

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("IP Glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            # Info about original source
            dcterms_source=String(
                "https://www.ipaustralia.gov.au/tools-resources/ip-glossary"
            ),
            publiclaw_sourceModified=mod_date,
            publiclaw_sourceCreator=String("IP Australia"),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85067167"),
                    rdfs_label=String("Intellectual property"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q131257"),
                    rdfs_label=String("Intellectual property"),
                ),
            ),
        ),
        entries=entries,
    )


def _parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    soup = make_soup(html)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),
            definition=Sentence(ensure_ends_with_period(normalize_nonempty(defn.text))),
        )
        for phrase, defn in raw_entries
    )


def _parse_mod_date(html: HtmlResponse) -> date:
    """
    Parse the modification date from HTML like this:

    <span class="date-display-single" property="dc:date" datatype="xsd:dateTime" content="2021-03-26T00:00:00+11:00">26 March 2021</span>
    """
    mod_date_str: str = cast(str, (
        html.selector.css("span.date-display-single").xpath("@content").get()  # type: ignore
    ))
    return datetime.fromisoformat(mod_date_str).date()
