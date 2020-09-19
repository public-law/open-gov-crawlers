from scrapy import Spider
from scrapy.http import Request, Response
from typing import Any, Dict

from public_law.parsers.ca.doj import parse_glossary


class DojGlossaries(Spider):
    name = "canada_doj_glossaries"
    start_urls = [
        "https://canada.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/2019/elf-esc/p7.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
        "https://www.justice.gc.ca/eng/cj-jp/ad-am/glos.html",
    ]

    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""
        yield parse_glossary(response)._asdict()
