from typing import cast

from scrapy.http.response.xml import XmlResponse

from public_law.test_util import *
from public_law.items.crs import Division
from public_law.parsers.usa.colorado.crs import parse_title_bang


# Divisions aren't parsing correctly.
TITLE_1 =  XmlResponse(body = fixture('usa', 'crs', "title01.xml"), url = "title01.xml", encoding = "utf-8")
PARSED_TITLE_1 = parse_title_bang(TITLE_1, null_logger)

# A Title with no Divisions.
TITLE_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
PARSED_TITLE_4 = parse_title_bang(TITLE_4, null_logger)

# A Title which uses Divisions.
TITLE_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
PARSED_TITLE_16 = parse_title_bang(TITLE_16, null_logger)


class TestWithNoDivisions:
    def test_correct_count(self):
        assert len(PARSED_TITLE_4.children) == 16


class TestParseErrors:
    def test_name(self):
        first_div = cast(Division, PARSED_TITLE_1.children[0])
        seventh_article = first_div.articles[6]

        assert seventh_article.name == "Internet-based Voting Pilot Program for Absent Uniformed Services Electors"

    def test_title_number(self):
        first_div = cast(Division, PARSED_TITLE_1.children[0])
        seventh_article = first_div.articles[6]

        assert seventh_article.title_number == "1"


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
        div_1_code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1              = div_1_code_of_crim_pro.articles[0]

        assert article_1.name == "General Provisions"


    def test_division_name_1(self):
        div_1_code_of_crim_pro = cast(Division, PARSED_TITLE_16.children[0])
        article_1              = div_1_code_of_crim_pro.articles[0]

        assert article_1.division_name == "Code of Criminal Procedure"
