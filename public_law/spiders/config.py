from dataclasses import dataclass
from typing import Type, Optional

from .utils import create_glossary_spider
from .base import BaseGlossarySpider


@dataclass
class SpiderConfig:
    """Configuration for a glossary spider."""
    name: str
    start_urls: list[str]
    parser_module: str
    description: Optional[str] = None


def register_spider(config: SpiderConfig) -> Type[BaseGlossarySpider]:
    """Register a spider from configuration."""
    return create_glossary_spider(
        name=config.name,
        start_urls=config.start_urls,
        parser_module_path=config.parser_module
    )


# Configuration registry
SPIDER_CONFIGS = {
    # Australia
    "aus_dv_glossary": SpiderConfig(
        name="aus_dv_glossary",
        start_urls=[
            "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
        ],
        parser_module="public_law.parsers.aus.dv_glossary",
        description="Family, domestic and sexual violence glossary from AIHW"
    ),

    "aus_ip_glossary": SpiderConfig(
        name="aus_ip_glossary",
        start_urls=[
            "https://www.ipaustralia.gov.au/understanding-ip/ip-glossary"],
        parser_module="public_law.parsers.aus.ip_glossary",
        description="Intellectual Property glossary from IP Australia"
    ),

    # USA
    "usa_uscis_glossary": SpiderConfig(
        name="usa_uscis_glossary",
        start_urls=["https://www.uscis.gov/tools/glossary"],
        parser_module="public_law.parsers.usa.uscis_glossary",
        description="USCIS immigration glossary"
    ),

    # Add more configurations as needed...
}


def get_spider_class(spider_name: str) -> Type[BaseGlossarySpider]:
    """Get a spider class by name from the configuration registry."""
    if spider_name not in SPIDER_CONFIGS:
        raise ValueError(f"Unknown spider: {spider_name}")

    config = SPIDER_CONFIGS[spider_name]
    return register_spider(config)
