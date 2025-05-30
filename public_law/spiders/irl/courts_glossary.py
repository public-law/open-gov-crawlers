from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "Ireland"
PUBLICATION_NAME = "Glossary of Legal Terms"


class IRLCourtsGlossary(AutoGlossarySpider):
    name = "irl_courts_glossary"
    start_urls = ["https://www.courts.ie/glossary"]
