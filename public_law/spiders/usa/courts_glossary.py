from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "US Courts Glossary"


class CourtsGlossary(AutoGlossarySpider):
    name = "usa_courts_glossary"
    start_urls = ["https://www.uscourts.gov/glossary"]
