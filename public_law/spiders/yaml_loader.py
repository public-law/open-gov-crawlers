import yaml
from pathlib import Path
from typing import Dict, Type, Any

from .utils import create_glossary_spider
from .base import BaseGlossarySpider


def load_spiders_from_yaml(yaml_path: str) -> Dict[str, Type[BaseGlossarySpider]]:
    """
    Load spider classes from a YAML configuration file.

    Args:
        yaml_path: Path to the YAML configuration file

    Returns:
        Dictionary mapping spider names to spider classes
    """
    config_path = Path(yaml_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {yaml_path}")

    with open(config_path, 'r') as f:
        config: Dict[str, Any] = yaml.safe_load(f)

    spiders: Dict[str, Type[BaseGlossarySpider]] = {}

    for spider_name, spider_config in config.get('spiders', {}).items():
        spider_class = create_glossary_spider(
            name=spider_config['name'],
            start_urls=spider_config['start_urls'],
            parser_module_path=spider_config['parser_module']
        )
        spiders[spider_name] = spider_class

    return spiders


# Auto-load spiders from default configuration
try:
    default_config_path = "glossary_spiders.yaml"
    auto_loaded_spiders = load_spiders_from_yaml(default_config_path)
except FileNotFoundError:
    auto_loaded_spiders: Dict[str, Type[BaseGlossarySpider]] = {}
