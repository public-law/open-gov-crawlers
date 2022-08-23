# pyright: reportSelfClsParameterName=false
from devtools import debug  # type: ignore
from more_itertools import first, last, nth
from scrapy.http.response.html import HtmlResponse

from public_law.dates import today
from public_law.metadata import Subject
from public_law.models.glossary import GlossaryParseResult
from public_law.text import URL, NonemptyString

# The System Under Test
from public_law.parsers.aus.dv_glossary import parse_glossary


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
    "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
)

GLOSSARY = parsed_fixture(filename="dv-glossary.html", jd_slug="aus", url=GLOSSARY_URL)

METADATA = GLOSSARY.metadata


class TestTheMetadata:
    def test_the_name(_):
        assert METADATA.dcterms_title == "Family, domestic and sexual violence glossary"

    def test_the_url(_):
        assert METADATA.dcterms_source == GLOSSARY_URL

    def test_the_author(_):
        assert METADATA.dcterms_creator == "https://public.law"

    def test_coverage(_):
        assert METADATA.dcterms_coverage == "AUS"

    def test_creator(_):
        assert (
            METADATA.publiclaw_sourceCreator
            == "Australia Institute of Health and Welfare"
        )

    def test_the_source_modified_date(_):
        assert METADATA.publiclaw_sourceModified == "unknown"

    def test_the_scrape_date(_):
        assert METADATA.dcterms_modified == today()

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
        assert first(GLOSSARY.entries).phrase == "arranged marriage"

    def test_definition(_):
        assert first(GLOSSARY.entries).definition == (
            "Distinct from <strong>forced marriage</strong>, an arranged marriage is organised "
            "by the families of both spouses, but consent is still present, "
            "and the spouses have the right to accept or reject the marriage arrangement."
        )

    def test_the_last_entry_phrase(_):
        assert last(GLOSSARY.entries).phrase == "vulnerable groups"

    def test_the_last_entry_definition(_):
        last_entry = last(GLOSSARY.entries)

        assert last_entry.definition == (
            "Population groups that are more likely to experience (or to have experienced) "
            "family, domestic and sexual violence, or that face additional barriers in "
            "coping with and recovering from family, domestic and sexual violence."
        )

    def test_proper_number_of_entries(_):
        assert len(tuple(GLOSSARY.entries)) == 37
