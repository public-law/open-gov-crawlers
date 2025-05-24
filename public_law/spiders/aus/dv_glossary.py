from ..enhanced_base import AutoGlossarySpider


class DVGlossary(AutoGlossarySpider):
    """Main DV Glossary spider using automatic parser resolution."""
    name = "aus_dv_glossary"
    start_urls = [
        "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
    ]
