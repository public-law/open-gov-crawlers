from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders._base.enhanced_base import EnhancedAutoGlossarySpider
from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String


class ParliamentaryGlossary(EnhancedAutoGlossarySpider):
    name       = "can_parliamentary_glossary"
    start_urls = [
        "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
    ]

    def get_metadata(self, response: HtmlResponse) -> Metadata:
        """Get metadata for the Canada Parliamentary Glossary."""
        source_url = URL(response.url)
        subjects = (
            Subject(
                uri=LoCSubject("sh85075807"),
                rdfs_label=String("Legislative bodies"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q35749"),
                rdfs_label=String("Parliament"),
            ),
        )

        return Metadata(
            dcterms_title=String(
                "Glossary of Parliamentary Terms for Intermediate Students"),
            dcterms_language="en",
            dcterms_coverage="CAN",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Parliament of Canada"),
            dcterms_subject=subjects,
        )
