from scrapy import Spider
from scrapy.http.response import Response
from typing import Any, Dict

from public_law.parsers.ca.doj import parse_glossary


class DojGlossaries(Spider):
    name = "canada_doj_glossaries"
    start_urls = [
        "https://laws-lois.justice.gc.ca/eng/glossary/",
        "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/aud-ver/2011/rc-pmr/01.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/2019/elf-esc/p7.html",
        "https://www.justice.gc.ca/eng/rp-pr/fl-lf/child-enfant/guide/glos.html",
        "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html",
        "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/calc/aa.html",
        "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/spag/p18.html",
    ]

    def parse(self, response: Response, **kwargs: Dict[str, Any]):
        """Framework callback which begins the parsing."""
        yield parse_glossary(response)._asdict()
