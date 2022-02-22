from scrapy.http import HtmlResponse
from public_law.parsers.ca.doj import parse_glossary, GlossarySourceParseResult
from public_law.dates import todays_date


def parsed_fixture(filename: str, url: str) -> GlossarySourceParseResult:
    with open(f"test/fixtures/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    parsed = parse_glossary(html)
    return parsed


def parsed_glossary() -> GlossarySourceParseResult:
    return parsed_fixture(
        "legal-aid-glossary.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
    )


def parsed_glossary_p11() -> GlossarySourceParseResult:
    return parsed_fixture(
        "p11.html", "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html"
    )


def parsed_glossary_glos() -> GlossarySourceParseResult:
    return parsed_fixture(
        "glos.html", "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html"
    )


def parsed_glossary_index() -> GlossarySourceParseResult:
    return parsed_fixture("index.html", "https://laws-lois.justice.gc.ca/eng/glossary/")


class TestParseGlossary:
    def setup(self):
        self.result = parsed_glossary()
        self.p11_result = parsed_glossary_p11()

    def test_gets_the_name(self):
        assert (
            self.result.name
            == "Legal Aid Program Evaluation, Final Report; Glossary of Legal Terms"
        )

    def test_gets_the_name_when_it_contains_an_anchor(self):
        assert (
            parsed_glossary_glos().name
            == "Managing Contact Difficulties: A Child-Centred Approach; GLOSSARY"
        )

    def test_gets_the_name_when_there_is_just_an_h1(self):
        assert parsed_glossary_index().name == "Glossary of technical terms"

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

    def test_parses_emphasized_text(self):
        definition_with_em = self.p11_result.entries[0].definition
        expected_definition = (
            "Legal term previously used in the <em>Divorce Act</em> to "
            "refer to the time a parent or other person spends with a "
            "child, usually not the parent with whom the child primarily "
            "lives."
        )

        assert definition_with_em == expected_definition
