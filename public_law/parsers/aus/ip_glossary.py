from scrapy.http.response.html import HtmlResponse
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import URL, LoCSubject, NonemptyString as String
from ...metadata import Metadata, Subject


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = []

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("IP Glossary"),
            dcterms_language="en",
            dcterms_coverage="NZL",
            # Info about original source
            dcterms_source=String(html.url),  # type: ignore
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("New Zealand Ministry of Justice"),
            publiclaw_readingEase=reading_ease(parsed_entries),
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
        entries=parsed_entries,
    )
