from more_itertools import first, last

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import glossary_fixture
from public_law.parsers.irl.courts_glossary import parse_glossary
from public_law.text import URL, NonemptyString


ORIG_URL = "https://www.courts.ie/glossary"
GLOSSARY = glossary_fixture("irl/ie.courts-glossary.html", ORIG_URL, parse_glossary)
METADATA = GLOSSARY.metadata
ENTRIES = tuple(GLOSSARY.entries)


def test_gets_the_name():
    assert METADATA.dcterms_title == "Glossary of Legal Terms"


def test_gets_the_url():
    assert METADATA.dcterms_source == "https://www.courts.ie/glossary"


def test_gets_the_author():
    assert METADATA.dcterms_creator == "https://public.law"


def test_gets_coverage():
    assert METADATA.dcterms_coverage == "IRL"


def test_gets_the_source_modified_date():
    assert METADATA.publiclaw_sourceModified == "unknown"


def test_gets_the_scrape_date():
    assert METADATA.dcterms_modified == today()


def test_subjects():
    assert METADATA.dcterms_subject == (
        Subject(
            uri=URL("http://id.loc.gov/authorities/subjects/sh85033571"),
            rdfs_label=NonemptyString("Courts"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q41487"),
            rdfs_label=NonemptyString("Court"),
        ),
    )


def test_definition():
    assert first(ENTRIES).definition == "A written statement made on oath."


def test_gets_proper_number_of_entries():
    assert len(ENTRIES) == 43


def test_gets_the_last_entry():
    last_entry = last(ENTRIES)

    assert last_entry.phrase == "Supervision order"
    assert last_entry.definition == (
        "An order allowing Tusla to monitor a child considered to be at risk. "
        "The child is not removed from his or her home environment. A supervision "
        "order is for a fixed period of time not longer than 12 months initially."
    )
