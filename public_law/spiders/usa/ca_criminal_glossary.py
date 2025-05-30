from public_law.spiders.enhanced_base import AutoGlossarySpider

class CaCriminalGlossary(AutoGlossarySpider):
    name       = "usa_criminal_glossary"
    start_urls = [ "https://www.sdcourt.ca.gov/sdcourt/criminal2/criminalglossary" ]
