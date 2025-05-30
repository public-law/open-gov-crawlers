from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "Design Examiners Manual Glossary"


class DesignIPGlossary(AutoGlossarySpider):
    name = "aus_designip_glossary"
    start_urls = [
        "http://manuals.ipaustralia.gov.au/design/glossary"
    ]
