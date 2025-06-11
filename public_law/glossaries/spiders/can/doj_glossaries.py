from datetime import date
from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata
from public_law.shared.utils.text import URL, NonemptyString
from public_law.shared.exceptions import ParseException
from public_law.glossaries.parsers.can.doj_glossaries import (
    configured_urls, SUBJECTS, parse_name, first_match
)


class DOJGlossariesSpider(EnhancedAutoGlossarySpider):
    name       = "can_doj_glossary"
    start_urls = configured_urls()

    def _resolve_parser_module(self) -> str:
        """Override to use the doj_glossaries parser module."""
        return "public_law.glossaries.parsers.can.doj_glossaries"

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the Canada DOJ Glossaries based on the response URL."""
        url = response.url
        name = parse_name(response)
        pub_date = first_match(response, "dl#wb-dtmd time::text", "Pub. date")

        match SUBJECTS.get(url):
            case tuple(subjects):
                dc_subject = subjects
            case None:
                raise ParseException(f"No subjects configured for {url}")

        return Metadata(
            dcterms_source=URL(url),
            dcterms_title=NonemptyString(name),
            dcterms_language="en",
            dcterms_coverage="CAN",
            publiclaw_sourceModified=date.fromisoformat(pub_date),
            publiclaw_sourceCreator=NonemptyString("Department of Justice Canada"),
            dcterms_subject=dc_subject,
        ) 
