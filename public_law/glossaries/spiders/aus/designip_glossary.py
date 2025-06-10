from datetime import date
from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String
from public_law.glossaries.parsers.aus.designip_glossary import parse_entries


class DesignIPGlossary(EnhancedAutoGlossarySpider):
    name       = "aus_designip_glossary"
    start_urls = ["http://manuals.ipaustralia.gov.au/design/glossary"]
    parse_function = parse_entries

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Generate metadata for the Australia Design IP Glossary."""
        return Metadata(
            dcterms_title=String("Design Examiners Manual Glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            dcterms_source=String(response.url),
            publiclaw_sourceModified=date(2024, 10, 14),
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
