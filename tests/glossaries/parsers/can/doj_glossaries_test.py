from datetime import date
from typing import cast

import pytest
from more_itertools import first, nth
from scrapy.http.response.html import HtmlResponse

from public_law.shared.utils.dates import today
from public_law.shared.utils.text import NonemptyString
from public_law.glossaries.models.glossary import (GlossaryEntry, GlossaryParseResult,
                                        glossary_fixture)
from public_law.glossaries.parsers.can.doj_glossaries import parse_entries

# Test URLs from the original fixtures
P7G_URL = "https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html"
P11_URL = "https://www.justice.gc.ca/eng/fl-df/parent/mp-fdp/p11.html"
GLOS_URL = "https://www.justice.gc.ca/eng/rp-pr/fl-lf/famil/2003_5/glos.html"
INDEX_URL = "https://laws-lois.justice.gc.ca/eng/glossary/"
P18_URL = "https://www.justice.gc.ca/eng/rp-pr/fl-lf/spousal-epoux/spag/p18.html"

@pytest.fixture(scope="module")
def p7g_response():
    """Load the HTML fixture for P7G DOJ Glossary"""
    with open("tests/fixtures/can/p7g.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=P7G_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def p11_response():
    """Load the HTML fixture for P11 DOJ Glossary"""
    with open("tests/fixtures/can/p11.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=P11_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def glos_response():
    """Load the HTML fixture for GLOS DOJ Glossary"""
    with open("tests/fixtures/can/glos.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=GLOS_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def index_response():
    """Load the HTML fixture for INDEX DOJ Glossary"""
    with open("tests/fixtures/can/index.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=INDEX_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture(scope="module")
def p18_response():
    """Load the HTML fixture for P18 DOJ Glossary"""
    with open("tests/fixtures/can/p18.html", "rb") as f:
        html_content = f.read()
    
    return HtmlResponse(
        url=P18_URL,
        body=html_content,
        encoding="utf-8",
    )

@pytest.fixture
def p7g_entries(p7g_response):
    return parse_entries(p7g_response)

@pytest.fixture
def p11_entries(p11_response):
    return parse_entries(p11_response)

@pytest.fixture
def glos_entries(glos_response):
    return parse_entries(glos_response)

@pytest.fixture
def index_entries(index_response):
    return parse_entries(index_response)

@pytest.fixture
def p18_entries(p18_response):
    return parse_entries(p18_response)


class TestParseEntries:
    def test_returns_tuple(self, p7g_entries):
        assert isinstance(p7g_entries, tuple)

    def test_proper_number_of_entries_p7g(self, p7g_entries):
        assert len(p7g_entries) == 36

    def test_all_entries_have_required_fields(self, p7g_entries):
        for entry in p7g_entries:
            assert isinstance(entry.phrase, NonemptyString)
            assert hasattr(entry, 'definition')
            assert len(entry.phrase) > 0
            assert len(entry.definition) > 0

    def test_phrase_does_not_end_with_colon(self, glos_entries):
        # First entry from GLOS should be "Alienated Parent" not "Alienated Parent:"
        first_entry = glos_entries[0]
        assert first_entry.phrase == "Alienated Parent"

    def test_parses_emphasized_text(self, p11_entries):
        definition_with_em = p11_entries[0].definition
        expected_definition = (
            "Legal term previously used in the <em>Divorce Act</em> to "
            "refer to the time a parent or other person spends with a "
            "child, usually not the parent with whom the child primarily "
            "lives."
        )
        assert definition_with_em == expected_definition

    def test_a_term_case_1(self, p7g_entries):
        entry = nth(p7g_entries, 2)
        assert entry.phrase == "Adjournment"
        assert entry.definition == "Postponement of a court hearing to another date."

    def test_parse_error_is_fixed_1(self, p18_entries):
        entry = list(p18_entries)[38]
        assert entry.phrase == "Ranges"
        assert entry.definition[-20:] == "Guidelines</em>.</p>"

    def test_parse_error_is_fixed_2(self, p18_entries):
        entry = list(p18_entries)[10]
        assert entry.phrase == "Divorce"
        assert entry.definition[-4:] == "</p>"

    def test_parse_error_is_fixed_3(self, p18_entries):
        entry = list(p18_entries)[1]
        assert entry.phrase == "Agreement"
        assert entry.definition[-4:] == "</p>"

    def test_parse_error_is_fixed_4(self, p18_entries):
        entry = list(p18_entries)[3]
        assert entry.phrase == "Child of the marriage"
        assert entry.definition[-4:] == "</p>"
