from public_law.spiders.enhanced_base import AutoGlossarySpider

JD_VERBOSE_NAME = "Australia"
PUBLICATION_NAME = "IP Glossary"


class IPGlossary(AutoGlossarySpider):
    name = "aus_ip_glossary"
    start_urls = [
        "https://raw.githubusercontent.com/public-law/datasets/master/Australia/ip-glossary.html"
    ]
