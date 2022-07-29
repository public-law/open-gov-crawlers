# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownMissingType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false

from datetime import date
from typing import cast

import pytest
from more_itertools import first, nth
from public_law.dates import today
from public_law.models.glossary import GlossaryEntry
from public_law.parsers.can.doj_glossaries import GlossaryParseResult, parse_glossary
from scrapy.http.response.html import HtmlResponse


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


@pytest.fixture
def p7g() -> GlossaryParseResult:
    return parsed_fixture(
        "p7g.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
    )


@pytest.fixture
def p11() -> GlossaryParseResult:
    return parsed_fixture(
        "p11.html", "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html"
    )


@pytest.fixture
def glos() -> GlossaryParseResult:
    return parsed_fixture(
        "glos.html", "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html"
    )


@pytest.fixture
def index() -> GlossaryParseResult:
    return parsed_fixture("index.html", "https://laws-lois.justice.gc.ca/eng/glossary/")


# @pytest.fixture
# def aa() -> GlossaryParseResult:
#     return parsed_fixture(
#         "aa.html",
#         "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/calc/aa.html",
#     )


def test_the_name_when_it_contains_an_anchor(glos):
    assert (
        glos.metadata.dcterms_title
        == "GLOSSARY - Managing Contact Difficulties: A Child-Centred Approach (2003-FCY-5E)"  # "Managing Contact Difficulties: A Child-Centred Approach; GLOSSARY"
    )


def test_phrase_does_not_end_with_colon(glos):
    assert first(glos.entries).phrase == "Alienated Parent"


def test_the_name_when_there_is_just_an_h1(index):
    assert index.metadata.dcterms_title == "Glossary"  # Unfortunately.


def test_parses_emphasized_text(p11):
    definition_with_em = first(p11.entries).definition
    expected_definition = (
        "Legal term previously used in the <em>Divorce Act</em> to "
        "refer to the time a parent or other person spends with a "
        "child, usually not the parent with whom the child primarily "
        "lives."
    )

    assert definition_with_em == expected_definition


def test_the_name(p7g):
    assert (
        p7g.metadata.dcterms_title
        == "GLOSSARY OF LEGAL TERMS - Legal Aid Program Evaluation"
    )


def test_the_url(p7g):
    assert (
        p7g.metadata.dcterms_source
        == "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
    )


def test_the_author(p7g):
    assert p7g.metadata.dcterms_creator == "https://public.law"


def test_the_scrape_date(p7g):
    assert p7g.metadata.publiclaw_sourceModified == date(2022, 5, 13)


def test_the_original_modification_date(p7g):
    assert p7g.metadata.dcterms_modified == today()


def test_proper_number_of_entries(p7g):
    assert len(tuple(p7g.entries)) == 36


def test_a_term_case_1(p7g):
    entry = cast(GlossaryEntry, nth(p7g.entries, 2))

    assert entry.phrase == "Adjournment"
    assert entry.definition == "Postponement of a court hearing to another date."


def test_reading_ease(p7g):
    assert p7g.metadata.publiclaw_readingEase == "Difficult"


def subj_strings(glossary):
    """
    Test helper: return the strings in a Glossary's subjects.
    """
    return tuple((s.uri, s.rdfs_label) for s in glossary.metadata.dcterms_subject)


class TestDcTermsSubject:
    def test_subject_p7g(self, p7g):
        assert subj_strings(p7g) == (
            ("http://id.loc.gov/authorities/subjects/sh85075720", "Legal aid"),
            ("https://www.wikidata.org/wiki/Q707748", "Legal aid"),
        )

    def test_subject_p11(self, p11):
        assert subj_strings(p11) == (
            (
                "http://id.loc.gov/authorities/subjects/sh85034952",
                "Custody of children",
            ),
            (
                "https://www.wikidata.org/wiki/Q638532",
                "Child custody",
            ),
        )

    def test_subject_glos(self, glos):
        assert subj_strings(glos) == (
            (
                "http://id.loc.gov/authorities/subjects/sh98001029",
                "Parental alienation syndrome",
            ),
            (
                "https://www.wikidata.org/wiki/Q1334131",
                "Parental alienation syndrome",
            ),
        )
