from public_law.spiders.enhanced_base import AutoGlossarySpider

class CourtsGlossary(AutoGlossarySpider):
    name       = "usa_courts_glossary"
    start_urls = ["https://www.uscourts.gov/glossary"]
