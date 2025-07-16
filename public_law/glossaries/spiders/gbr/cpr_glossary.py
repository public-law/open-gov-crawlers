from datetime import datetime
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders._base.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject, WikidataTopic
from public_law.shared.utils.text import NonemptyString as String

class CPRGlossarySpider(EnhancedAutoGlossarySpider):
    """
    Spider for the UK Criminal Procedure Rules glossary.
    """
    name       = "gbr_cpr_glossary"
    start_urls = ["https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
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
            dcterms_source=source_url,
            publiclaw_sourceModified=self.parse_mod_date(response),
            publiclaw_sourceCreator=String("The National Archives"),
            dcterms_subject=subjects,
        )

    @staticmethod
    def parse_mod_date(response: HtmlResponse):
        import typed_soup
        from bs4 import Tag
        empty_tag = Tag(None, None, "")
        soup = typed_soup.from_response(response)
        matching_paragraph = next(
            (p for p in soup("p") if "in force at" in p.get_text()),
            empty_tag
        )
        date_str = (
            matching_paragraph
            .get_text()
            .split("in force at")[1]
            .strip()
            .split(",")[0]
            .strip()
        )
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            return "unknown"
