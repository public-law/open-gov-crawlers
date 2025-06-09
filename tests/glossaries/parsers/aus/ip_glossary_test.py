from datetime import date

from more_itertools import first, last

from public_law.shared.utils.dates import today
from public_law.shared.models.metadata import Subject
from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.aus.ip_glossary import parse_glossary
from public_law.shared.utils.text import URL, NonemptyString

ORIG_URL = "https://www.ipaustralia.gov.au/tools-resources/ip-glossary"
GLOSSARY = glossary_fixture("aus/ip-glossary.html", ORIG_URL, parse_glossary)
METADATA = GLOSSARY.metadata

#
# Tests for metadata.
#


def test_the_name():
    assert METADATA.dcterms_title == "IP Glossary"


def test_url():
    assert METADATA.dcterms_source == ORIG_URL


def test_author():
    assert METADATA.dcterms_creator == "https://public.law"


def test_coverage():
    assert METADATA.dcterms_coverage == "AUS"


def test_scrape_date():
    assert METADATA.dcterms_modified == today()


def test_source_modified_date():
    assert METADATA.publiclaw_sourceModified == date(2021, 3, 26)


def test_subjects():
    assert METADATA.dcterms_subject == (
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


def test_phrase():
    assert first(GLOSSARY.entries).phrase == "Assignee"


def test_definition():
    assert (
        first(GLOSSARY.entries).definition
        == "The person/s or corporate body to whom all or limited rights under an IP right are legally transferred."
    )


def test_proper_number_of_entries():
    assert len(tuple(GLOSSARY.entries)) == 53


def test_last_entry():
    last_entry = last(GLOSSARY.entries)

    assert last_entry.phrase == "Voluntary request for examination"
    assert last_entry.definition == (
        "You as the applicant for an IP right (e.g. innovation patent) "
        "request the registrar to conduct an examination of your application. "
        "This is normally done if you believe that your rights have been infringed."
    )
