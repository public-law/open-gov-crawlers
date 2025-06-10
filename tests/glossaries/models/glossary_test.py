from typing import Any, cast
import pytest

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.nzl import justice_glossary

ORIG_URL = "https://www.justice.govt.nz/about/glossary/"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("nzl/justice-glossary.html", ORIG_URL, justice_glossary.parse_glossary)


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
