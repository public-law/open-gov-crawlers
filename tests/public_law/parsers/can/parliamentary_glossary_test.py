# pyright: reportSelfClsParameterName=false
from devtools import debug  # type: ignore
from more_itertools import first, last
from scrapy.http.response.html import HtmlResponse

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult
from public_law.text import URL, NonemptyString

# The System Under Test
from public_law.parsers.can.parliamentary_glossary import parse_glossary


def parsed_fixture(filename: str, jd_slug: str, url: URL) -> GlossaryParseResult:
    """
    Create a GlossaryParseResult using the three required parameters.
    """
    with open(f"tests/fixtures/{jd_slug}/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


GLOSSARY_URL = URL(
    "https://lop.parl.ca/About/Parliament/Education/glossary-intermediate-students-e.html"
)

GLOSSARY = parsed_fixture(
    filename="parliamentary-glossary.html",
    jd_slug="can",
    url=GLOSSARY_URL
    )

METADATA = GLOSSARY.metadata


class TestTheMetadata:
    def test_the_name(_):
        assert METADATA.dcterms_title == 'Glossary of Parliamentary Terms for Intermediate Students'

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
                uri=URL("http://id.loc.gov/authorities/subjects/sh85075807"),
                rdfs_label=NonemptyString("Legislative bodies"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q35749"),
                rdfs_label=NonemptyString("Parliament"),
            ),
        )


class TestTheEntries:
    def test_phrase(_):
        assert first(GLOSSARY.entries).phrase == "adjournment proceedings"

    def test_definition(_):
        assert first(GLOSSARY.entries).definition == (
            "A 30-minute period before the end of a daily sitting in the "
            "House of Commons when Members of Parliament can debate matters "
            "raised in Question Period or written questions that have not "
            "been answered within 45 days."
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(GLOSSARY.entries)) == 86

    def test_the_last_entry(_):
        last_entry = last(GLOSSARY.entries)

        assert last_entry.phrase == "whip"
        assert last_entry.definition == (
            "The Member who is responsible for keeping other "
            "members of the same party informed about House "
            "business and ensuring their attendance in the "
            "Chamber, especially when a vote is anticipated."
        )
