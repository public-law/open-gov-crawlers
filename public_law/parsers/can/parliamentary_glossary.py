# pyright: reportSelfClsParameterName=false

from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult
from public_law.text import URL, NonemptyString

from public_law.parsers.can.parliamentary_glossary import parse_glossary


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/can/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


GLOSSARY_URL = URL(
    "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
)

GLOSSARY = parsed_fixture(filename="parliamentary-glossary.html", url=GLOSSARY_URL)

METADATA = GLOSSARY.metadata


class TestTheMetadata:
    def test_the_name(_):
        assert METADATA.dcterms_title == "Glossary of Legal Terms"

    def test_the_url(_):
        assert METADATA.dcterms_source == GLOSSARY_URL

    def test_the_author(_):
        assert METADATA.dcterms_creator == "https://public.law"

    def test_coverage(_):
        assert METADATA.dcterms_coverage == "USA"

    def test_the_source_modified_date(_):
        assert METADATA.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(_):
        assert METADATA.dcterms_modified == today()

    def test_reading_ease(_):
        assert METADATA.publiclaw_readingEase == "Fairly difficult"

    def test_subjects(_):
        assert METADATA.dcterms_subject == (
            Subject(
                uri=URL("http://id.loc.gov/authorities/subjects/sh85033575"),
                rdfs_label=NonemptyString("Courts--United States"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q194907"),
                rdfs_label=NonemptyString("United States federal courts"),
            ),
        )


class TestTheEntries:
    def test_phrase(_):
        assert first(GLOSSARY.entries).phrase == "Acquittal"

    def test_definition(_):
        assert first(GLOSSARY.entries).definition == (
            "A jury verdict that a criminal defendant is not guilty, "
            "or the finding of a judge that the evidence is insufficient "
            "to support a conviction."
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(GLOSSARY.entries)) == 237

    def test_the_last_entry(_):
        last_entry = last(GLOSSARY.entries)

        assert last_entry.phrase == "Writ of certiorari"
        assert last_entry.definition == (
            "An order issued by the U.S. Supreme Court directing "
            "the lower court to transmit records for a case which "
            "it will hear on appeal."
        )
