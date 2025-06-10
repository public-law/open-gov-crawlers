from scrapy.http.response.html import HtmlResponse

from public_law.shared.spiders.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic
from public_law.shared.utils.text import NonemptyString as String
from public_law.glossaries.parsers.gbr.cpr_glossary import parse_mod_date


class CPRGlossarySpider(EnhancedAutoGlossarySpider):
    """
    Spider for the UK Criminal Procedure Rules glossary.
    """
    name       = "gbr_cpr_glossary"
    start_urls = ["https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the Great Britain CPR Glossary."""
        source_url = URL(response.url)
        subjects = (
            Subject(LoCSubject("sh85033571"), String("Courts")),
            Subject(WikidataTopic("Q41487"),  String("Court")),
            Subject(LoCSubject("sh85034086"), String("Criminal Procedure")),
            Subject(WikidataTopic("Q146071"), String("Criminal Procedure")),
        )

        return Metadata(
            dcterms_title=String("Criminal Procedure Rules Glossary"),
            dcterms_language="en",
            dcterms_coverage="GBR",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified=parse_mod_date(response),
            publiclaw_sourceCreator=String("The National Archives"),
            dcterms_subject=subjects,
        )
