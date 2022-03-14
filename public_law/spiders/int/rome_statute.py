from scrapy import Spider
from scrapy.http import Response, HtmlResponse
from typing import Any, Dict

from public_law.parsers.int.rome_statute import title


class RomeStatute(Spider):
    name = "rome_statute"
    start_urls = [
        "https://www.icc-cpi.int/resource-library/Pages/core-legal-texts.aspx",
    ]

    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""
        assert isinstance(response, HtmlResponse)

        yield parse_glossary(response)._asdict()
