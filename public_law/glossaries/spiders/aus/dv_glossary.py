from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String
from public_law.glossaries.parsers.aus.dv_glossary import parse_entries


class DVGlossary(EnhancedAutoGlossarySpider):
    """Main DV Glossary spider using automatic parser resolution."""
    name = "aus_dv_glossary"
    start_urls = [
        "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
    ]
    parse_function = parse_entries

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Generate metadata for the Australia DV Glossary."""
        return Metadata(
            dcterms_title=String("Family, domestic and sexual violence glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            # Info about original source
            dcterms_source=String(response.url),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Australian Institute of Health and Welfare"),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85047071"),
                    rdfs_label=String("Family violence"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q156537"),
                    rdfs_label=String("Domestic violence"),
                ),
            ),
        )
