from scrapy.selector import Selector

from public_law.parsers import (
    opinion_date_to_iso8601,
    parse_ag_opinion,
    OpinionParseResult,
)


def parsed_opinion(filename: str) -> OpinionParseResult:
    with open(f"test/fixtures/{filename}") as f:
        html = Selector(text=f.read())
        return parse_ag_opinion(html)


class TestOpinionDateToISO8601:
    def test_sample_1(self):
        opinion_date = "OCTOBER 02, 2017"
        assert opinion_date_to_iso8601(opinion_date) == "2017-10-02"


class TestParseAgOpinion:
    def setup(self):
        self.result = parsed_opinion("opinion-2017-3.html")

    def test_gets_the_summary(self):
        expected_summary = (
            "Updating of crimes and offenses for which "
            "the Georgia Crime Information Center is "
            "authorized to collect and file fingerprints."
        )
        assert self.result.summary == expected_summary

    def test_gets_the_title(self):
        assert self.result.title == "Official Opinion 2017-3"

    def test_gets_is_official(self):
        assert self.result.is_official

    def test_gets_the_date(self):
        assert self.result.date == "2017-10-02"
