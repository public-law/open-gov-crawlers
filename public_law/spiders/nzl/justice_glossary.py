from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "New Zealand"
PUBLICATION_NAME = "Glossary"


class NZLJusticeGlossary(AutoGlossarySpider):
    name = "nzl_justice_glossary"
    start_urls = ["https://www.justice.govt.nz/about/glossary/"]
