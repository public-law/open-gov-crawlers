from typing import cast

from datetime import date
from more_itertools import first, nth

from scrapy.http.response.html import HtmlResponse
from public_law.parsers.can.doj_glossaries import parse_glossary, GlossaryParseResult
from public_law.dates import today
from public_law.models.glossary import GlossaryEntry


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


def parsed_glossary() -> GlossaryParseResult:
    return parsed_fixture(
        "p7g.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
    )


def parsed_glossary_p11() -> GlossaryParseResult:
    return parsed_fixture(
        "p11.html", "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html"
    )


def parsed_glossary_glos() -> GlossaryParseResult:
    return parsed_fixture(
        "glos.html", "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html"
    )


def parsed_glossary_index() -> GlossaryParseResult:
    return parsed_fixture("index.html", "https://laws-lois.justice.gc.ca/eng/glossary/")


class TestParseGlossary:
    # pyright: reportUninitializedInstanceVariable=false
    def setup(self):
        self.result = parsed_glossary()
        self.p11_result = parsed_glossary_p11()

    def test_gets_the_name(self):
        assert (
            self.result.metadata.dcterms_title
            == "GLOSSARY OF LEGAL TERMS - Legal Aid Program Evaluation"
        )

    def test_gets_the_name_when_it_contains_an_anchor(self):
        assert (
            parsed_glossary_glos().metadata.dcterms_title
            == "GLOSSARY - Managing Contact Difficulties: A Child-Centred Approach (2003-FCY-5E)"  # "Managing Contact Difficulties: A Child-Centred Approach; GLOSSARY"
        )

    def test_phrase_does_not_end_with_colon(self):
        assert first(parsed_glossary_glos().entries).phrase == "Alienated Parent"

    def test_gets_the_name_when_there_is_just_an_h1(self):
        assert (
            parsed_glossary_index().metadata.dcterms_title == "Glossary"
        )  # Unfortunately.

    def test_gets_the_url(self):
        assert (
            self.result.metadata.dcterms_source
            == "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
        )

    def test_gets_the_author(self):
        assert self.result.metadata.dcterms_creator == "https://public.law"

    def test_gets_the_scrape_date(self):
        assert self.result.metadata.publiclaw_sourceModified == date(2022, 5, 13)

    def test_gets_the_original_modification_date(self):
        assert self.result.metadata.dcterms_modified == today()

    def test_gets_proper_number_of_entries(self):
        assert len(tuple(self.result.entries)) == 36

    def test_gets_a_term_case_1(self):
        entry = cast(GlossaryEntry, nth(self.result.entries, 2))

        assert entry.phrase == "Adjournment"
        assert entry.definition == "Postponement of a court hearing to another date."

    def test_parses_emphasized_text(self):
        definition_with_em = first(self.p11_result.entries).definition
        expected_definition = (
            "Legal term previously used in the <em>Divorce Act</em> to "
            "refer to the time a parent or other person spends with a "
            "child, usually not the parent with whom the child primarily "
            "lives."
        )

        assert definition_with_em == expected_definition
