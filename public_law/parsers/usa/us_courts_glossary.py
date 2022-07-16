from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = tuple(__parse_entries(html))

    # pyright: reportUnknownMemberType=false
    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="USA",
            # Info about original source
            dcterms_source=String("https://www.uscourts.gov/glossary"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("United States Courts"),
            publiclaw_readingEase=reading_ease(parsed_entries),
        ),
        entries=parsed_entries,
    )


def __parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    soup = make_soup(html)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),
            definition=Sentence(ensure_ends_with_period(normalize_nonempty(defn.text))),
        )
        for phrase, defn in raw_entries
    )
