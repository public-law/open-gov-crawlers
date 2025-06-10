from datetime import date
import pytest

from more_itertools import first, last

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.aus.ip_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.ipaustralia.gov.au/tools-resources/ip-glossary"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("aus/ip-glossary.html", ORIG_URL, parse_glossary)

@pytest.fixture
def metadata(glossary):
    return glossary.metadata

#
# Tests for metadata.
#


def test_the_name(metadata):
    assert metadata.dcterms_title == "IP Glossary"


def test_url(metadata):
    assert metadata.dcterms_source == ORIG_URL


def test_author(metadata):
    assert metadata.dcterms_creator == "https://public.law"


def test_coverage(metadata):
    assert metadata.dcterms_coverage == "AUS"


def test_scrape_date(metadata):
    assert metadata.dcterms_modified == today()


def test_source_modified_date(metadata):
    assert metadata.publiclaw_sourceModified == date(2021, 3, 26)


def test_subjects(metadata):
    assert metadata.dcterms_subject == (
        Subject(
            uri=URL("http://id.loc.gov/authorities/subjects/sh85067167"),
            rdfs_label=NonemptyString("Intellectual property"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q131257"),
            rdfs_label=NonemptyString("Intellectual property"),
        ),
    )


#
# Tests for content.
#


def test_phrase(glossary):
    assert first(glossary.entries).phrase == "Assignee"


def test_definition(glossary):
    assert (
        first(glossary.entries).definition
        == "The person/s or corporate body to whom all or limited rights under an IP right are legally transferred."
    )


def test_proper_number_of_entries(glossary):
    assert len(glossary.entries) == 53


def test_last_entry(glossary):
    last_entry = last(glossary.entries)

    assert last_entry.phrase == "Voluntary request for examination"
    assert last_entry.definition == (
        "You as the applicant for an IP right (e.g. innovation patent) "
        "request the registrar to conduct an examination of your application. "
        "This is normally done if you believe that your rights have been infringed."
    )
