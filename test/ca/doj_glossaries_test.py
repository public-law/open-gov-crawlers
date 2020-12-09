from scrapy.http import HtmlResponse
from public_law.parsers.ca.doj import parse_glossary, GlossarySourceParseResult
from public_law.dates import todays_date


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

    def test_gets_proper_number_of_entries(self):
        assert len(self.result.entries) == 36

    def test_gets_a_term_case_1(self):
        term = self.result.entries[2]
        assert term.phrase == "Adjournment"
        assert term.definition == "postponement of a court hearing to another date."
