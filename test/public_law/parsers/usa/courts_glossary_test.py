from datetime import date
from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.parsers.us.courts_glossary import (
    parse_glossary,
    GlossarySourceParseResult,
)
from public_law.dates import today


def parsed_fixture(filename: str, url: str) -> GlossarySourceParseResult:
    with open(f"test/fixtures/usa/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


@fixture
def parsed_glossary_uscourts() -> GlossarySourceParseResult:
    return parsed_fixture(
        filename="gov.uscourts-glossary.html", url="https://www.uscourts.gov/glossary"
    )


class TestParseGlossary:
    @mark.skip(reason="Not implemented yet")
    def test_gets_the_name(self):
        assert (
            self.result.metadata.dcterms_title
            == "GLOSSARY OF LEGAL TERMS - Legal Aid Program Evaluation"
        )

    @mark.skip(reason="Not implemented yet")
    def test_gets_the_name_when_it_contains_an_anchor(self):
        assert (
            parsed_glossary_glos().metadata.dcterms_title
            == "GLOSSARY - Managing Contact Difficulties: A Child-Centred Approach (2003-FCY-5E)"  # "Managing Contact Difficulties: A Child-Centred Approach; GLOSSARY"
        )

    @mark.skip(reason="Not implemented yet")
    def test_phrase_does_not_end_with_colon(self):
        assert parsed_glossary_glos().entries[0].phrase == "Alienated Parent"

    @mark.skip(reason="Not implemented yet")
    def test_gets_the_name_when_there_is_just_an_h1(self):
        assert (
            parsed_glossary_index().metadata.dcterms_title == "Glossary"
        )  # Unfortunately.

    @mark.skip(reason="Not implemented yet")
    def test_gets_the_url(self):
        assert (
            self.result.metadata.dcterms_source
            == "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
        )

    @mark.skip(reason="Not implemented yet")
    def test_gets_the_author(self):
        assert self.result.metadata.dcterms_creator == "https://public.law"

    @mark.skip(reason="Not implemented yet")
    def test_gets_the_scrape_date(self):
        assert self.result.metadata.publiclaw_sourceModified == date(2022, 5, 13)

    @mark.skip(reason="Not implemented yet")
    def test_gets_the_original_modification_date(self):
        assert self.result.metadata.dcterms_modified == today()

    @mark.skip(reason="Not implemented yet")
    def test_gets_proper_number_of_entries(self):
        assert len(self.result.entries) == 36

    @mark.skip(reason="Not implemented yet")
    def test_gets_a_term_case_1(self):
        term = self.result.entries[2]
        assert term.phrase == "Adjournment"
        assert term.definition == "Postponement of a court hearing to another date."

    @mark.skip(reason="Not implemented yet")
    def test_parses_emphasized_text(self):
        definition_with_em = self.p11_result.entries[0].definition
        expected_definition = (
            "Legal term previously used in the <em>Divorce Act</em> to "
            "refer to the time a parent or other person spends with a "
            "child, usually not the parent with whom the child primarily "
            "lives."
        )

        assert definition_with_em == expected_definition
