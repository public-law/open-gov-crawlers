from public_law.metadata import Metadata
from public_law.text import NonemptyString as S
from public_law.dates import today


class TestMetadata:
    def test_creates_expected_dict_1(self):
        metadata = Metadata(
            dc_creator=S("The creator"),
            dc_source=S("https://a.b.c"),
            dc_title=S("The Title"),
            dc_language="en",
            dcterms_modified=today(),
            dcterms_coverage=S('Canada'),
            publiclaw_sourceModified=today(),
        )
        generated_dict = metadata.as_dublin_core_dict()

        # fmt: off
        expected_dict = {
            "dc:creator":         "The creator",
            "dc:language":        "en",
            "dc:source":          "https://a.b.c",
            "dc:title":           "The Title",
            "dc:type":            "Dataset",
            "dcterms:coverage":   "Canada",
            "dcterms:format":     "application/json",
            "dcterms:license":    "https://creativecommons.org/licenses/by/4.0/",
            "dcterms:modified":   today(),
            "publiclaw:sourceModified": today(),
        }

        assert generated_dict == expected_dict

    def test_creates_expected_dict_2(self):
        metadata = Metadata(
            dc_creator=S("The creator"),
            dc_source=S("https://a.b.c"),
            dc_title=S("The Title"),
            dc_language="en",
            dcterms_modified=today(),
            dcterms_coverage=S('Canada'),
            publiclaw_sourceModified=today(),
        )
        generated_dict = dict(metadata)

        # fmt: off
        expected_dict = {
            "dc:creator":               "The creator",
            "dc:language":              "en",
            "dc:source":                "https://a.b.c",
            "dc:title":                 "The Title",
            "dc:type":                  "Dataset",
            "dcterms:coverage":         "Canada",
            "dcterms:format":           "application/json",
            "dcterms:license":          "https://creativecommons.org/licenses/by/4.0/",
            "dcterms:modified":         today(),
            "publiclaw:sourceModified": today(),
        }

        assert generated_dict == expected_dict
