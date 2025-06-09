from public_law.shared.spiders.enhanced_base import AutoGlossarySpider


class USCISGlossary(AutoGlossarySpider):
    name       = "usa_uscis_glossary"
    start_urls = ["https://www.uscis.gov/tools/glossary"]
