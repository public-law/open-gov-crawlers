from public_law.metadata import Metadata
from public_law.text import NonemptyString as S
from public_law.dates import today


class TestMetadata:
    def test_creates_expected_dict_1(self):
        metadata = Metadata(
            dcterms_source=S("https://a.b.c"),
            dcterms_title=S("The Title"),
            dcterms_language="en",
            dcterms_modified=today(),
            dcterms_coverage=S('Canada'),
            publiclaw_sourceModified=today(),
            publiclaw_sourceCreator=S("Some Canadian Agency"),
        )
        generated_dict = metadata.as_dublin_core_dict()

        # fmt: off
        expected_dict = {
            "dcterms:creator":          "https://public.law",
            "dcterms:language":         "en",
            "dcterms:source":           "https://a.b.c",
            "dcterms:title":            "The Title",
            "dcterms:type":             "Dataset",
            "dcterms:coverage":         "Canada",
            "dcterms:format":           "application/json",
            "dcterms:license":          "https://creativecommons.org/licenses/by/4.0/",
            "dcterms:modified":         today(),
            "publiclaw:sourceModified": today(),
            "publiclaw:sourceCreator":  "Some Canadian Agency",
        }

        assert generated_dict == expected_dict

    def test_creates_expected_dict_2(self):
        metadata = Metadata(
            dcterms_source=S("https://a.b.c"),
            dcterms_title=S("The Title"),
            dcterms_language="en",
            dcterms_modified=today(),
            dcterms_coverage=S('Canada'),
            publiclaw_sourceModified=today(),
            publiclaw_sourceCreator=S("Some Canadian Agency"),
        )
        generated_dict = dict(metadata)

        # fmt: off
        expected_dict = {
            "dcterms:creator":          "https://public.law",
            "dcterms:language":         "en",
            "dcterms:source":           "https://a.b.c",
            "dcterms:title":            "The Title",
            "dcterms:type":             "Dataset",
            "dcterms:coverage":         "Canada",
            "dcterms:format":           "application/json",
            "dcterms:license":          "https://creativecommons.org/licenses/by/4.0/",
            "dcterms:modified":         today(),
            "publiclaw:sourceModified": today(),
            "publiclaw:sourceCreator":  "Some Canadian Agency",
        }

        assert generated_dict == expected_dict
