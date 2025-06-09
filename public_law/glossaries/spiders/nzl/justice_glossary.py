from public_law.shared.spiders.enhanced_base import AutoGlossarySpider

class NZLJusticeGlossary(AutoGlossarySpider):
    name       = "nzl_justice_glossary"
    start_urls = ["https://www.justice.govt.nz/about/glossary/"]
