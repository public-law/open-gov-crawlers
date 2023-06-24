from typing import cast

from scrapy.http.response.xml import XmlResponse

from public_law.test_util import fixture
from public_law.items.crs import Division
from public_law.parsers.usa.colorado.crs import parse_title_bang



# A Title with no Divisions.
TITLE_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
PARSED_TITLE_4 = parse_title_bang(TITLE_4)

# A Title which uses Divisions.
TITLE_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
PARSED_TITLE_16 = parse_title_bang(TITLE_16)


class TestParseArticles:
    def test_correct_number_of_articles_in_a_division_1(self):
        # Title 16 contains eight Divisions.
        #   The first Division is _Code of Criminal Procedure_
        #       This Division contains 22 Articles.
        div_1_code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])

        assert div_1_code_of_crim_pro.name          == "Code of Criminal Procedure"
        assert len(div_1_code_of_crim_pro.articles) == 22


    def test_correct_number_of_articles_in_a_division_2(self):
        division_2 = cast(Division, PARSED_TITLE_16.children[1])
        
        assert division_2.name          == "Uniform Mandatory Disposition of Detainers Act"
        assert len(division_2.articles) == 1


    def test_article_number_1(self):
        code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1        = code_of_crim_pro.articles[0]

        assert article_1.number == "1"


    def test_article_name_1(self):
        code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1        = code_of_crim_pro.articles[0]

        assert article_1.name == "General Provisions"
