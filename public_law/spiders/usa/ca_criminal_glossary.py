from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "USA"
PUBLICATION_NAME = "Criminal Glossary"


class CaCriminalGlossary(AutoGlossarySpider):
    name = "usa_criminal_glossary"
    start_urls = [
        "https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary"
    ]
