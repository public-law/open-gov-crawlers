from public_law.spiders.enhanced_base import AutoGlossarySpider

class IPGlossary(AutoGlossarySpider):
    name       = "aus_ip_glossary"
    start_urls = [
        "https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html"
    ]
