from datetime import date
from typing import cast

import pytest
from more_itertools import first, nth

from public_law.dates import today
from public_law.models.glossary import (GlossaryEntry, GlossaryParseResult,
                                        glossary_fixture)
from public_law.parsers.can.doj_glossaries import parse_glossary


@pytest.fixture
def p7g() -> GlossaryParseResult:
    return glossary_fixture(
        "can/p7g.html",
        "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
        parse_glossary,
    )


@pytest.fixture
def p11() -> GlossaryParseResult:
    return glossary_fixture(
        "can/p11.html",
        "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html",
        parse_glossary,
    )


GLOS = glossary_fixture(
    "can/glos.html",
    "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html",
    parse_glossary,
)


@pytest.fixture
def index() -> GlossaryParseResult:
    return glossary_fixture(
        "can/index.html",
        "https://laws-lois.justice.gc.ca/eng/glossary/",
        parse_glossary,
    )


@pytest.fixture
def p18() -> GlossaryParseResult:
    return glossary_fixture(
        "can/p18.html",
        "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/spag/p18.html",
        parse_glossary,
    )


#
# Metadata tests
#


class TestDctermsTitle:
    def test_when_it_contains_an_anchor(self):
        assert (
            GLOS.metadata.dcterms_title
            == "Glossary - Managing Contact Difficulties: A Child-Centred Approach (2003-FCY-5E)"
        )

    def test_when_there_is_just_an_h1(self, index: GlossaryParseResult):
        assert index.metadata.dcterms_title == "Glossary"  # Unfortunately.

    def test_all_caps_title_correctly_formatted(self, p18: GlossaryParseResult):
        assert (
            p18.metadata.dcterms_title
            == "Glossary of Terms - Spousal Support Advisory Guidelines July 2008"
        )

    def test_the_title(self, p7g: GlossaryParseResult):
        assert (
            p7g.metadata.dcterms_title
            == "Glossary of Legal Terms - Legal Aid Program Evaluation"
        )


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

    def test_subject_glos(self):
        assert subj_strings(GLOS) == (
            (
                "http://id.loc.gov/authorities/subjects/sh98001029",
                "Parental alienation syndrome",
            ),
            (
                "https://www.wikidata.org/wiki/Q1334131",
                "Parental alienation syndrome",
            ),
        )


def test_phrase_does_not_end_with_colon():
    assert first(GLOS.entries).phrase == "Alienated Parent"


def test_parses_emphasized_text(p11: GlossaryParseResult):
    definition_with_em = first(p11.entries).definition
    expected_definition = (
        "Legal term previously used in the <em>Divorce Act</em> to "
        "refer to the time a parent or other person spends with a "
        "child, usually not the parent with whom the child primarily "
        "lives."
    )

    assert definition_with_em == expected_definition


def test_parse_error_is_fixed_1(p18: GlossaryParseResult):
    entry = list(p18.entries)[38]

    assert entry.phrase == "Ranges"
    assert entry.definition[-20:] == "Guidelines</em>.</p>"


def test_parse_error_is_fixed_2(p18: GlossaryParseResult):
    entry = list(p18.entries)[10]

    assert entry.phrase == "Divorce"
    assert entry.definition[-4:] == "</p>"


def test_parse_error_is_fixed_3(p18: GlossaryParseResult):
    entry = list(p18.entries)[1]

    assert entry.phrase == "Agreement"
    assert entry.definition[-4:] == "</p>"


def test_parse_error_is_fixed_4(p18: GlossaryParseResult):
    entry = list(p18.entries)[3]

    assert entry.phrase == "Child of the marriage"
    assert entry.definition[-4:] == "</p>"


def test_the_url(p7g: GlossaryParseResult):
    assert (
        p7g.metadata.dcterms_source
        == "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
    )


def test_the_author(p7g: GlossaryParseResult):
    assert p7g.metadata.dcterms_creator == "https://public.law"


def test_the_scrape_date(p7g: GlossaryParseResult):
    assert p7g.metadata.publiclaw_sourceModified == date(2022, 5, 13)


def test_the_original_modification_date(p7g: GlossaryParseResult):
    assert p7g.metadata.dcterms_modified == today()


def test_proper_number_of_entries(p7g: GlossaryParseResult):
    assert len(tuple(p7g.entries)) == 36


def test_a_term_case_1(p7g: GlossaryParseResult):
    entry = cast(GlossaryEntry, nth(p7g.entries, 2))

    assert entry.phrase == "Adjournment"
    assert entry.definition == "Postponement of a court hearing to another date."


def subj_strings(glossary: GlossaryParseResult):
    """
    Test helper: return the strings in a Glossary's subjects.
    """
    return tuple((s.uri, s.rdfs_label) for s in glossary.metadata.dcterms_subject)
