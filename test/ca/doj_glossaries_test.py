from typing_extensions import Protocol

from datetime import datetime, date
import pytz

from scrapy.http import HtmlResponse
from public_law.parsers.ca.doj import parse_glossary, GlossarySourceParseResult


class SimpleTimezone(Protocol):
    def localize(self, dt: datetime) -> date:
        ...


def todays_date() -> str:
    mountain: SimpleTimezone = pytz.timezone("US/Mountain")
    fmt = "%Y-%m-%d"
    return mountain.localize(datetime.now()).strftime(fmt)


def parsed_glossary() -> GlossarySourceParseResult:
    filename = "legal-aid-glossary.html"

    with open(f"test/fixtures/{filename}") as f:
        html = HtmlResponse(
            url="https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
            body=f.read(),
            encoding="UTF-8",
        )

    parsed = parse_glossary(html)
    return parsed


class TestParseGlossary:
    def setup(self):
        self.result = parsed_glossary()

    def test_gets_the_name(self):
        assert (
            self.result.name
            == "Legal Aid Program Evaluation, Final Report; Glossary of Legal Terms"
        )

    def test_gets_the_url(self):
        assert (
            self.result.source_url
            == "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
        )

    def test_gets_the_author(self):
        assert self.result.author == "Department of Justice Canada"

    def test_gets_the_publication_date(self):
        assert self.result.pub_date == "2015-01-07"

    def test_gets_the_scrape_date(self):
        assert self.result.scrape_date == todays_date()
