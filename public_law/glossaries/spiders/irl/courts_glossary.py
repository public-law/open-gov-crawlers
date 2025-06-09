from public_law.shared.spiders.enhanced_base import AutoGlossarySpider

class IRLCourtsGlossary(AutoGlossarySpider):
    name       = "irl_courts_glossary"
    start_urls = ["https://www.courts.ie/glossary"]
