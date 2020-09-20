from scrapy import Spider
from scrapy.http import Response, HtmlResponse
from typing import Any, Dict

from public_law.parsers.ca.doj import parse_glossary


class DojGlossaries(Spider):
    name = "canada_doj_glossaries"
    start_urls = [
        "https://canada.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/2019/elf-esc/p7.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
    ]

    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""
        assert isinstance(response, HtmlResponse)
        yield parse_glossary(response)._asdict()
