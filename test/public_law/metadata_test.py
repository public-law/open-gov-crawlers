from public_law.metadata import Metadata
from public_law.text import NonemptyString as S
from public_law.dates import todays_date


class TestMetadata:
    def test_creates_expected_dict(self):
        metadata = Metadata(
            dc_creator=S("The creator"),
            dc_identifier=S("https://x.y.z"),
            dc_source=S("https://a.b.c"),
            dc_title=S("The Title"),
            dc_language=S("en-US"),
        )
        generated_dict = metadata.as_dict()

        expected_dict = {
            "dc:creator": "The creator",
            "dc:identifier": "https://x.y.z",
            "dc:language": "en-US",
            "dc:publisher": "Public.Law",
            "dc:source": "https://a.b.c",
            "dc:title": "The Title",
            "dc:type": "text",
            "dcterms:license": "https://creativecommons.org/licenses/by/4.0/",
            "dcterms:modified": todays_date(),
        }

        assert generated_dict == expected_dict