from public_law.shared.spiders.enhanced_base import AutoGlossarySpider


class EurLexGlossary(AutoGlossarySpider):
    """
    Spider for the EUR-Lex Glossary of Summaries.
    
    This spider crawls individual glossary term pages. For a complete crawl,
    you would need to run this with multiple URLs or extend it to follow 
    the index page links.
    """
    name = "eur_eurlex_glossary"
    start_urls = [
        "https://eur-lex.europa.eu/EN/legal-content/glossary/abstention-constructive-positive-abstention.html"
    ] 
