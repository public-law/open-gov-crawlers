from public_law.spiders.enhanced_base import AutoGlossarySpider


class FPRGlossarySpider(AutoGlossarySpider):
    """
    Spider for the UK Family Procedure Rules glossary.
    """
    name       = "gbr_fpr_glossary"
    start_urls = ["https://www.justice.gov.uk/courts/procedure-rules/family/backmatter/fpr_glossary"]
