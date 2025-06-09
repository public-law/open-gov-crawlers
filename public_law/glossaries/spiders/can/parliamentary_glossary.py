from public_law.shared.spiders.enhanced_base import AutoGlossarySpider

class ParliamentaryGlossary(AutoGlossarySpider):
    name       = "can_parliamentary_glossary"
    start_urls = [
        "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
    ]
