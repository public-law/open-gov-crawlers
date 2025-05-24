from ..utils import create_glossary_spider

# Declarative spider creation
DVGlossary = create_glossary_spider(
    name="aus_dv_glossary",
    start_urls=[
        "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
    ],
    parser_module_path="public_law.parsers.aus.dv_glossary"
)
