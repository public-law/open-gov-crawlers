from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "Canada"
PUBLICATION_NAME = "Glossary of Parliamentary Terms for Intermediate Students"


class ParliamentaryGlossary(AutoGlossarySpider):
    name = "can_parliamentary_glossary"
    start_urls = [
        "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
    ]
