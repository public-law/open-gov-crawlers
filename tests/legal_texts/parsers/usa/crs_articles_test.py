from typing import cast

import pytest
from scrapy.http.response.xml import XmlResponse

from public_law.legal_texts.models.crs import Article, Division, Subdivision, Title
from public_law.legal_texts.parsers.usa.colorado.crs import parse_title_bang
from public_law.test_util import fixture, null_logger


class TestParseErrors:
    # Divisions aren't parsing correctly.
    @pytest.fixture(scope="module")
    def parsed_title_1(self) -> Title:
        print(":fire: parsing title 1")
        title_1 =  XmlResponse(body = fixture('usa', 'crs', "title01.xml"), url = "title01.xml", encoding = "utf-8")
        return parse_title_bang(title_1, null_logger)


    def test_name(self, parsed_title_1):
        first_div = cast(Division, parsed_title_1.children[0])
        seventh_article = first_div.children[6]

        assert seventh_article.name == "Internet-based Voting Pilot Program for Absent Uniformed Services Electors"

    def test_title_number(self, parsed_title_1):
        first_div = cast(Division, parsed_title_1.children[0])
        seventh_article = first_div.children[6]

        assert seventh_article.title_number == "1"


class TestFromSubdivision:
    @pytest.fixture(scope="module")
    def parsed_title_7(self) -> Title:
        print(":fire: parsing title 7")
        title_7 = XmlResponse(body = fixture('usa', 'crs', "title07.xml"), url = "title07.xml", encoding = "utf-8")
        return parse_title_bang(title_7, null_logger)


    def test_correct_number(self, parsed_title_7):
        div_8 =    cast(Division, parsed_title_7.children[7])
        assert div_8.name == 'Corporations - Continued'

        subdiv_1 = cast(Subdivision, div_8.children[0])
        assert subdiv_1.name == 'Colorado Business Corporations'

        assert len(subdiv_1.articles) == 17


    def test_correct_div_name(self, parsed_title_7):
        div_8    = cast(Division, parsed_title_7.children[7])
        subdiv_1 = cast(Subdivision, div_8.children[0])
        art_1    = subdiv_1.articles[0]

        assert art_1.division_name == div_8.name


    def test_correct_subdiv_name(self, parsed_title_7):
        div_8    = cast(Division, parsed_title_7.children[7])
        subdiv_1 = cast(Subdivision, div_8.children[0])
        art_1    = subdiv_1.articles[0]

        assert art_1.subdivision_name == subdiv_1.name


    def test_we_got_article_55(self, parsed_title_7):
        div_2 = cast(Division, parsed_title_7.children[1])
        assert div_2.kind == 'Division'
        assert div_2.name == 'Associations'

        art_55 = cast(Article, div_2.children[0])
        assert art_55.kind == 'Article'

        assert art_55.number == '55'
        assert art_55.name   == "Cooperatives - General"


    def test_we_got_article_56(self, parsed_title_7):
        div_2      = cast(Division, parsed_title_7.children[1])
        article_56 = cast(Article, div_2.children[1])

        assert article_56.name == "Cooperatives"


    def test_repealed_statute_number(self, parsed_title_7):
        last_div         = cast(Division, parsed_title_7.children[-1])
        subdiv           = cast(Subdivision, last_div.children[-2])
        article_104      = subdiv.articles[3]

        assert last_div.name == 'Corporations - Continued'
        assert subdiv.name   == 'Colorado Business Corporations'
        assert article_104.number == '104'


    def test_repealed_statute_name(self, parsed_title_7):
        last_div         = cast(Division, parsed_title_7.children[-1])
        subdiv           = cast(Subdivision, last_div.children[-2])
        article_104      = subdiv.articles[3]

        assert last_div.name    == 'Corporations - Continued'
        assert subdiv.name      == 'Colorado Business Corporations'
        assert article_104.name == 'Name (Repealed)'


    def test_we_get_articles_101_to_117(self, parsed_title_7):
        expected_numbers = [str(i) for i in range(101, 118)]
        last_div         = cast(Division, parsed_title_7.children[-1])
        subdiv           = cast(Subdivision, last_div.children[-2])
        article_numbers  = [a.number for a in subdiv.articles]

        assert last_div.name    == 'Corporations - Continued'
        assert subdiv.name      == 'Colorado Business Corporations'
        assert article_numbers  == expected_numbers


    def test_we_get_articles_121_to_137(self, parsed_title_7):
        expected_numbers = [str(i) for i in range(121, 138)]
        last_div         = cast(Division, parsed_title_7.children[-1])
        last_subdiv      = cast(Subdivision, last_div.children[-1])
        article_numbers  = [a.number for a in last_subdiv.articles]

        assert last_div.name    == 'Corporations - Continued'
        assert last_subdiv.name == 'Nonprofit Corporations'
        assert article_numbers  == expected_numbers


class TestParseArticles:
    @pytest.fixture(scope="module")
    def parsed_title_16(self) -> Title:
        print(":fire: parsing title 16")
        title_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
        return parse_title_bang(title_16, null_logger)


    def test_correct_number_of_articles_in_a_division_1(self, parsed_title_16):
        # Title 16 contains eight Divisions.
        #   The first Division is _Code of Criminal Procedure_
        #       This Division contains 22 Articles.
        div_1_code_of_crim_pro = cast(Division, parsed_title_16.children[0])

        assert div_1_code_of_crim_pro.name          == "Code of Criminal Procedure"
        assert len(div_1_code_of_crim_pro.children) == 22


    def test_correct_number_of_articles_in_a_division_2(self, parsed_title_16):
        division_2 = cast(Division, parsed_title_16.children[1])
        
        assert division_2.name          == "Uniform Mandatory Disposition of Detainers Act"
        assert len(division_2.children) == 1


    def test_article_number_1(self, parsed_title_16):
        code_of_crim_pro = cast(Division, parsed_title_16.children[0])
        article_1        = cast(Article, code_of_crim_pro.children[0])

        assert article_1.number == "1"


    def test_article_name_1(self, parsed_title_16):
        div_1_code_of_crim_pro = cast(Division, parsed_title_16.children[0])
        article_1              = div_1_code_of_crim_pro.children[0]

        assert article_1.name == "General Provisions"


    def test_division_name_1(self, parsed_title_16):
        div_1_code_of_crim_pro = cast(Division, parsed_title_16.children[0])
        article_1              = cast(Article, div_1_code_of_crim_pro.children[0])

        assert article_1.division_name == "Code of Criminal Procedure"


class TestWithNoDivisions:
    # A Title with no Divisions.

    @pytest.fixture(scope="module")
    def parsed_title_4(self) -> Title:
        print(":fire: parsing title 4")
        title_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
        return parse_title_bang(title_4, null_logger)


    def test_correct_count(self, parsed_title_4):
        assert len(parsed_title_4.children) == 16


    def test_theyre_all_articles(self, parsed_title_4):
        for child in parsed_title_4.children:
            assert child.kind == "Article"


    @pytest.fixture(scope="module")
    def parsed_article_1(self, parsed_title_4) -> Article:
        print(":fire: parsing article 1")
        return cast(Article, parsed_title_4.children[0])


    def test_a_name(self, parsed_article_1):
        assert parsed_article_1.name == "General Provisions"

    def test_a_number(self, parsed_article_1):
        assert parsed_article_1.number == "1"

    def test_a_title_number(self, parsed_article_1):
        assert parsed_article_1.title_number == "4"

    def test_a_division_name(self, parsed_article_1):
        assert parsed_article_1.division_name is None

    @pytest.fixture(scope="module")
    def parsed_article_3(self, parsed_title_4) -> Article:
        print(":fire: parsing article 3")
        return cast(Article, parsed_title_4.children[2])

    def test_a_name_2(self, parsed_article_3):
        assert parsed_article_3.name == "Leases"

    def test_a_number_2(self, parsed_article_3):
        assert parsed_article_3.number == "2.5"

    def test_a_title_number_2(self, parsed_article_3):
        assert parsed_article_3.title_number == "4"

    def test_a_division_name_2(self, parsed_article_3):
        assert parsed_article_3.division_name is None


    # This should be the last article in Title 4.
    @pytest.fixture(scope="module")
    def parsed_article_11(self, parsed_title_4) -> Article:
        print(":fire: parsing article 11")
        return cast(Article, parsed_title_4.children[-1])

    def test_a_name_3(self, parsed_article_11):
        assert parsed_article_11.name == "Fees (Repealed)"

    def test_a_number_3(self, parsed_article_11):
        assert parsed_article_11.number == "11"

    def test_a_title_number_3(self, parsed_article_11):
        assert parsed_article_11.title_number == "4"
    
    def test_a_division_name_3(self, parsed_article_11):
        assert parsed_article_11.division_name is None
