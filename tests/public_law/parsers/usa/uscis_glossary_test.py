from more_itertools import first, last
from pytest import fixture, mark
from scrapy.http.response.html import HtmlResponse

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.usa.uscis_glossary import parse_glossary
from public_law.text import URL, NonemptyString


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/usa/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


def parsed_glossary() -> GlossaryParseResult:
    return parsed_fixture(
        filename="uscis-glossary.html",
        url="https://www.uscis.gov/tools/glossary",
    )


GLOSSARY = parsed_glossary()
METADATA = GLOSSARY.metadata


#
# Metadata tests
#

def test_gets_the_name():
    assert METADATA.dcterms_title == "USCIS Glossary"


def test_gets_the_url():
    assert METADATA.dcterms_source == "https://www.uscis.gov/tools/glossary"


def test_gets_the_author():
    assert METADATA.dcterms_creator == "https://public.law"


def test_the_original_creator():
    assert METADATA.publiclaw_sourceCreator == "U.S. Citizenship and Immigration Services"


def test_gets_coverage():
    assert METADATA.dcterms_coverage == "USA"


def test_gets_the_source_modified_date():
    assert METADATA.publiclaw_sourceModified == "unknown"


def test_gets_the_scrape_date():
    assert METADATA.dcterms_modified == today()


def test_subjects():
    assert METADATA.dcterms_subject == (
        Subject(
            uri=URL("http://id.loc.gov/authorities/subjects/sh85042790"),
            rdfs_label=NonemptyString("Emigration and immigration law"),
        ),
        Subject(
            uri=URL("https://www.wikidata.org/wiki/Q231147"),
            rdfs_label=NonemptyString("immigration law"),
        ),
    )


#
# Content tests
#

def test_phrase():
    assert first(GLOSSARY.entries).phrase == "Alien Registration Number"


def test_definition():
    assert (
        first(GLOSSARY.entries).definition == (
            '<p>A unique seven-, eight- or nine-digit number assigned to a noncitizen '
            'by the Department of Homeland Security. Also see '
            '<a aria-label="Show glossary definition for USCIS Number" data-entity-substitution="canonical" data-entity-type="node" data-lang="en" data-linktype="glossary" data-nid="50674" href="#">USCIS Number</a>.'
            '</p>'
        )
    )


def test_gets_proper_number_of_entries():
    assert len(tuple(GLOSSARY.entries)) == 266


def test_gets_the_last_phrase():
    last_entry = last(GLOSSARY.entries)

    assert last_entry.phrase == "Withdrawal"


def test_gets_the_last_definition():
    last_entry = last(GLOSSARY.entries)

    assert last_entry.definition == (
        '<p>This is an arriving noncitizen’s voluntary retraction of an application '
        'for admission to the United States in lieu of a removal hearing before an '
        'immigration judge or an expedited removal.</p>'
    )
