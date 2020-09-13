from typing import Any, IO
from scrapy.selector import Selector

from public_law.parsers import opinion_date_to_iso8601, parse_ag_opinion


def fixture(filename: str) -> IO[Any]:
    return open(f"test/fixtures/{filename}")


class TestOpinionDateToISO8601:
    def test_sample_1(self):
        opinion_date = "OCTOBER 02, 2017"
        assert opinion_date_to_iso8601(opinion_date) == "2017-10-02"


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

    def test_gets_is_official(self):
        with fixture("opinion-2017-3.html") as f:
            html = Selector(text=f.read())
            result = parse_ag_opinion(html)

            assert result.is_official