from datetime import date, datetime
from typing import cast
from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String
from public_law.glossaries.parsers.aus.ip_glossary import parse_entries


class IPGlossary(EnhancedAutoGlossarySpider):
    name       = "aus_ip_glossary"
    start_urls = [
        "https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html"
    ]
    parse_function = parse_entries

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Generate metadata for the Australia IP Glossary."""
        mod_date = self._parse_mod_date(response)
        
        return Metadata(
            dcterms_title=String("IP Glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            # Info about original source
            dcterms_source=String("https://www.ipaustralia.gov.au/tools-resources/ip-glossary"),
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
        )

    def _parse_mod_date(self, html: HtmlResponse) -> date:
        """
        Parse the modification date from HTML like this:

        <span class="date-display-single" property="dc:date" datatype="xsd:dateTime" content="2021-03-26T00:00:00+11:00">26 March 2021</span>
        """
        mod_date_str: str = cast(str, (
            html.selector.css("span.date-display-single").xpath("@content").get()
        ))
        return datetime.fromisoformat(mod_date_str).date()
