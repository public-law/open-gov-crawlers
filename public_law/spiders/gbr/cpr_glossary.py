from public_law.spiders.enhanced_base import AutoGlossarySpider


class CPRGlossarySpider(AutoGlossarySpider):
    """
    Spider for the UK Criminal Procedure Rules glossary.
    """
    name = "gbr_cpr_glossary"
    start_urls = [
        "https://www.legislation.gov.uk/uksi/2020/759/part/Glossary?view=plain"
    ]
