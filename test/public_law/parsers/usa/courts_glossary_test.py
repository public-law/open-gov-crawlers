from datetime import date
from scrapy.http.response.html import HtmlResponse
from pytest import fixture, mark

from public_law.dates import today
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.us.courts_glossary import parse_glossary


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"test/fixtures/usa/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


@fixture
def parsed_glossary_uscourts() -> GlossaryParseResult:
    return parsed_fixture(
        filename="gov.uscourts-glossary.html", url="https://www.uscourts.gov/glossary"
    )


def test_gets_the_name(parsed_glossary_uscourts: GlossaryParseResult):
    assert (
        parsed_glossary_uscourts.metadata.dcterms_title
        == "Glossary of Legal Terms | United States Courts"
    )


@mark.skip(reason="Not implemented yet")
def test_phrase_does_not_end_with_colon(
    parsed_glossary_uscourts: GlossaryParseResult,
):
    assert parsed_glossary_uscourts.entries[0].phrase == "Alienated Parent"


@mark.skip(reason="Not implemented yet")
def test_gets_the_url(parsed_glossary_uscourts: GlossaryParseResult):
    assert (
        parsed_glossary_uscourts.metadata.dcterms_source
        == "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
    )


@mark.skip(reason="Not implemented yet")
def test_gets_the_author(parsed_glossary_uscourts: GlossaryParseResult):
    assert parsed_glossary_uscourts.metadata.dcterms_creator == "https://public.law"


@mark.skip(reason="Not implemented yet")
def test_gets_the_scrape_date(parsed_glossary_uscourts: GlossaryParseResult):
    assert parsed_glossary_uscourts.metadata.publiclaw_sourceModified == date(
        2022, 5, 13
    )


@mark.skip(reason="Not implemented yet")
def test_gets_the_original_modification_date(
    parsed_glossary_uscourts: GlossaryParseResult,
):
    assert parsed_glossary_uscourts.metadata.dcterms_modified == today()


@mark.skip(reason="Not implemented yet")
def test_gets_proper_number_of_entries(
    parsed_glossary_uscourts: GlossaryParseResult,
):
    assert len(parsed_glossary_uscourts.entries) == 36


@mark.skip(reason="Not implemented yet")
def test_gets_a_term_case_1(parsed_glossary_uscourts: GlossaryParseResult):
    entry = parsed_glossary_uscourts.entries[2]
    assert entry.phrase == "Adjournment"
    assert entry.definition == "Postponement of a court hearing to another date."


@mark.skip(reason="Not implemented yet")
def test_parses_emphasized_text(parsed_glossary_uscourts: GlossaryParseResult):
    definition_with_em = self.p11_result.entries[0].definition
    expected_definition = (
        "Legal term previously used in the <em>Divorce Act</em> to "
        "refer to the time a parent or other person spends with a "
        "child, usually not the parent with whom the child primarily "
        "lives."
    )

    assert definition_with_em == expected_definition
