from typing import Any, IO
from scrapy.selector import Selector

from public_law.parsers import parse_ag_opinion


def fixture(filename: str) -> IO[Any]:
    return open(f"test/fixtures/{filename}")


class TestParseAgOpinion:
    def test_gets_the_summary(self):
        with fixture("opinion-2017-3.html") as f:
            html = Selector(text=f.read())

            expected_summary = (
                "Updating of crimes and offenses for which "
                "the Georgia Crime Information Center is "
                "authorized to collect and file fingerprints."
            )
            result = parse_ag_opinion(html)

            assert result.summary == expected_summary

    def test_gets_the_title(self):
        with fixture("opinion-2017-3.html") as f:
            html = Selector(text=f.read())
            result = parse_ag_opinion(html)

            expected_title = "Official Opinion 2017-3"
            assert result.title == expected_title