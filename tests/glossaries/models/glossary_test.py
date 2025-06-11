from typing import Any, cast
import pytest
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.spiders.nzl.justice_glossary import JusticeGlossarySpider

ORIG_URL = "https://www.justice.govt.nz/about/glossary/"

@pytest.fixture(scope="module")
def glossary():
    with open("tests/fixtures/nzl/justice-glossary.html", "rb") as f:
        html_content = f.read()
    response = HtmlResponse(
        url=ORIG_URL,
        body=html_content,
        encoding="utf-8",
    )
    spider = JusticeGlossarySpider()
    return spider.parse_glossary(response)


class TestAsDict:
    def test_returns_real_data(self, glossary):
        entries = cast(list[dict[str, Any]], glossary.asdict()["entries"])
        assert entries[0]["phrase"] == "acquit"

    def test_converts_to_dict(self, glossary):
        assert glossary.asdict()

    def test_dict_func_doesnt_change_it(self, glossary):
        assert glossary.asdict() == dict(glossary.asdict())

    def test_dict_func_is_equivalent(self, glossary):
        assert glossary.asdict() == dict(glossary)

    def test_has_renamed_metadata_key(self, glossary):
        assert "dcterms:subject" in glossary.asdict()["metadata"]
