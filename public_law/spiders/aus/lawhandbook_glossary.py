from public_law.spiders.enhanced_base import AutoGlossarySpider


class LawHandbookGlossary(AutoGlossarySpider):
    name = "aus_lawhandbook_glossary"
    start_urls = ["https://lawhandbook.sa.gov.au/go01.php"]
