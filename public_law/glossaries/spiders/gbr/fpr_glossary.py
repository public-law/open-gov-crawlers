from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic
from public_law.shared.utils.text import NonemptyString as String
from public_law.glossaries.parsers.gbr.fpr_glossary import parse_mod_date


class FPRGlossarySpider(EnhancedAutoGlossarySpider):
    """
    Spider for the UK Family Procedure Rules glossary.
    """
    name       = "gbr_fpr_glossary"
    start_urls = ["https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the Great Britain FPR Glossary."""
        source_url = URL(response.url)
        subjects = (
            Subject(LoCSubject("sh85033571"), String("Courts")),
            Subject(WikidataTopic("Q41487"),  String("Court")),
        )

        return Metadata(
            dcterms_title=String("Family Procedure Rules Glossary"),
            dcterms_language="en",
            dcterms_coverage="GBR",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified=parse_mod_date(response),
            publiclaw_sourceCreator=String("Ministry of Justice"),
            dcterms_subject=subjects,
        )
