from typing import Any, cast
import pytest

from public_law.glossaries.models.glossary import glossary_fixture
from public_law.glossaries.parsers.can import doj_glossaries

ORIG_URL = "https://laws-lois.justice.gc.ca/eng/glossary/"

@pytest.fixture(scope="module")
def glossary():
    return glossary_fixture("can/index.html", ORIG_URL, doj_glossaries.parse_glossary)


class TestAsDict:
    def test_returns_real_data(self, glossary):
        entries = cast(list[dict[str, Any]], glossary.asdict()["entries"])
        assert entries[0]["phrase"] == "C.R.C."

    def test_converts_to_dict(self, glossary):
        assert glossary.asdict()

    def test_dict_func_doesnt_change_it(self, glossary):
        assert glossary.asdict() == dict(glossary.asdict())

    def test_dict_func_is_equivalent(self, glossary):
        assert glossary.asdict() == dict(glossary)

    def test_has_renamed_metadata_key(self, glossary):
        assert "dcterms:subject" in glossary.asdict()["metadata"]
