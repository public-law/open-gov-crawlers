import re
from dataclasses import asdict
from typing import Any, Dict

from public_law.parsers.int.rome_statute import articles, new_metadata, parts
from scrapy import Spider
from scrapy.http import Response  # type: ignore


class RomeStatute(Spider):
    name = "rome_statute"
    start_urls = [
        "https://www.icc-cpi.int/resource-library",
    ]

    def parse(self, response: Response, **_kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""

        # TODO: Implement both a tree output and flat output?
        #       And allow the user to choose the output type via
        #       an option to Scrapy.

        #       Tree output:
        #         yield {"title": title(pdf_url), "parts": parts(pdf_url)}

        for url in start_page_urls(response):
            if "Rome-Statute.pdf" in url:  # Only parse the English version
                yield {"metadata": new_metadata(url).as_dict()}

                for part in parts(url):
                    yield {"part": part._asdict()}

                for article in articles(url):
                    yield {"article": article._asdict()}


#
# Pure helper functions
#


def start_page_urls(response: Response) -> list[str]:
    anchors = response.css("h2#coreICCtexts + p + div").css("a").getall()[:4]
    relative_urls = [re.findall(r'"(.+)"', a)[0] for a in anchors]
    absolute_urls = ["https://www.icc-cpi.int" + url for url in relative_urls]

    return absolute_urls
