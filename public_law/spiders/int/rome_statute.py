import re
from scrapy import Spider
from scrapy.http import Response, HtmlResponse
from typing import Any, Dict

from public_law.parsers.int.rome_statute import title


class RomeStatute(Spider):
    name = "rome_statute"
    start_urls = [
        "https://www.icc-cpi.int/resource-library#coreICCtexts",
    ]

    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""
        assert isinstance(response, HtmlResponse)

        pdf_urls = start_page_urls(response)

        # yield parse_glossary(response)._asdict()


#
# Pure helper functions
#


def start_page_urls(response: Response) -> list[str]:
    anchors = response.css("h2#coreICCtexts + p + div").css("a").getall()[:4]
    relative_urls = [re.findall(r'"(.+)"', a)[0] for a in anchors]
    absolute_urls = ["https://www.icc-cpi.int" + url for url in relative_urls]

    return absolute_urls
