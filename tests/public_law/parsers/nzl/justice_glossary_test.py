# pyright: reportSelfClsParameterName=false

from more_itertools import first, last
from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import glossary_fixture
from public_law.parsers.nzl.justice_glossary import parse_glossary
from public_law.text import URL, NonemptyString


ORIG_URL = "https://www.justice.govt.nz/about/glossary/"
GLOSSARY = glossary_fixture(
    "nzl/nz.govt.justice-glossary.html",
    ORIG_URL,
    parse_glossary,
)
METADATA = GLOSSARY.metadata
ENTRIES = tuple(GLOSSARY.entries)


class TestMetadata:
    def test_name(_):
        assert METADATA.dcterms_title == "Glossary"

    def test_url(_):
        assert METADATA.dcterms_source == ORIG_URL

    def test_author(_):
        assert METADATA.dcterms_creator == "https://public.law"

    def test_coverage(_):
        assert METADATA.dcterms_coverage == "NZL"

    def test_source_modified_date(_):
        assert METADATA.publiclaw_sourceModified == "unknown"

    def test_scrape_date(_):
        assert METADATA.dcterms_modified == today()

    def test_subjects(_):
        assert METADATA.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85071120"),
                rdfs_label=NonemptyString("Justice, Administration of"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q16514399"),
                rdfs_label=NonemptyString("Administration of justice"),
            ),
        )


class TestEntries:
    def test_phrase(_):
        assert first(ENTRIES).phrase == "acquit"

    def test_definition(_):
        assert (
            first(ENTRIES).definition
            == "To decide officially in court that a person is not guilty."
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(ENTRIES)) == 154

    def test_last_entry(_):
        last_entry = last(ENTRIES)

        assert last_entry.phrase == "Youth Court"
        assert last_entry.definition == (
            "The Youth Court has jurisdiction to deal with "
            "young people charged with criminal offences."
        )
