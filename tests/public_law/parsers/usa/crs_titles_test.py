from scrapy.http.response.xml import XmlResponse

from public_law.test_util import fixture
from public_law.parsers.usa.colorado.crs import parse_title_bang


# A Title with no Divisions.
TITLE_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
PARSED_TITLE_4 = parse_title_bang(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
PARSED_TITLE_16 = parse_title_bang(TITLE_16)



class TestParseTitles:
    def test_title_name_1(self):
        assert PARSED_TITLE_16.name == "Criminal Proceedings"

    def test_title_name_2(self):
        assert PARSED_TITLE_4.name == "Uniform Commercial Code"


    def test_title_url_1(self):
        assert (
            PARSED_TITLE_16.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-16.pdf"
        )

    def test_title_url_2(self):
        assert (
            PARSED_TITLE_4.source_url
            == "https://leg.colorado.gov/sites/default/files/images/olls/crs2022-title-04.pdf"
        )


    def test_title_number_1(self):
        assert PARSED_TITLE_16.number == "16"

    def test_title_number_2(self):
        assert PARSED_TITLE_4.number == "4"
