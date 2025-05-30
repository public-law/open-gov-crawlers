from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "USCIS Glossary"


class USCISGlossary(AutoGlossarySpider):
    name = "usa_uscis_glossary"
    start_urls = ["https://www.uscis.gov/tools/glossary"]
