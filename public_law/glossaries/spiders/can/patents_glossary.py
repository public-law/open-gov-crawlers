from public_law.shared.spiders.enhanced_base import AutoGlossarySpider


class PatentsGlossarySpider(AutoGlossarySpider):
    name       = "can_patents_glossary"
    start_urls = ["https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/glossary"]
