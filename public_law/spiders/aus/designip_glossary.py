from public_law.spiders.enhanced_base import AutoGlossarySpider

class DesignIPGlossary(AutoGlossarySpider):
    name       = "aus_designip_glossary"
    start_urls = ["http://manuals.ipaustralia.gov.au/design/glossary"]
