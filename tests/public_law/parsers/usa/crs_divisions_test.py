# pyright: reportPrivateUsage=false


import pytest
from typing import cast

from scrapy.http.response.xml import XmlResponse

from public_law.test_util import *
from public_law.parsers.usa.colorado.crs import parse_title_bang
from public_law.parsers.usa.colorado.crs_divisions import _has_subdivisions
from public_law.items.crs import Division, Subdivision


# Divisions aren't parsing correctly.
TITLE_1 =  XmlResponse(body = fixture('usa', 'crs', "title01.xml"), url = "title01.xml", encoding = "utf-8")
PARSED_TITLE_1 = parse_title_bang(TITLE_1, null_logger)

# A Title with no Divisions.
TITLE_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
PARSED_TITLE_4 = parse_title_bang(TITLE_4, null_logger)

# A Title which uses Divisions.
TITLE_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
PARSED_TITLE_16 = parse_title_bang(TITLE_16, null_logger)

# A Title with Divisions and Subdivisions.
TITLE_07 = XmlResponse(body = fixture('usa', 'crs', "title07.xml"), url = "title07.xml", encoding = "utf-8")
PARSED_TITLE_07 = parse_title_bang(TITLE_07, null_logger)


class TestHasSubdivisions:
    def test_when_it_does(self):
        assert _has_subdivisions(TITLE_07)

    def test_when_it_does_not(self):
        assert not _has_subdivisions(TITLE_16)


class TestParseErrors:
    @pytest.mark.skip
    def test_name(self):
        divs = PARSED_TITLE_1.children
        assert divs[0].name == "General, Primary, Recall, and Congressional Vacancy Elections"

    @pytest.mark.skip
    def test_title_number(self):
        divs = PARSED_TITLE_1.children
        assert divs[0].title_number == "1"


class TestParseTitle7:
    # $ grep '<T-DIV>' tmp/sources/CRSDADA20220915/TITLES/title07.xml
    #
    # <T-DIV>CORPORATIONS</T-DIV>
    #   <T-DIV>Colorado Corporation Code</T-DIV>
    #   <T-DIV>Nonprofit Corporations</T-DIV>
    #   <T-DIV>Special Purpose Corporations</T-DIV>
    #   <T-DIV>Religious and Benevolent Organizations</T-DIV>
    # <T-DIV>ASSOCIATIONS</T-DIV>
    # <T-DIV>PARTNERSHIPS</T-DIV>
    # <T-DIV>TRADEMARKS AND BUSINESS NAMES</T-DIV>
    # <T-DIV>TRADE SECRETS</T-DIV>
    # <T-DIV>LIMITED LIABILITY COMPANIES</T-DIV>
    # <T-DIV>CORPORATIONS AND ASSOCIATIONS</T-DIV>
    # <T-DIV>CORPORATIONS - Continued</T-DIV>
    #   <T-DIV>Colorado Business Corporations</T-DIV>
    #   <T-DIV>Nonprofit Corporations</T-DIV>

    def test_correct_number_of_divisions(self):
        assert len(PARSED_TITLE_07.children) == 8
        for putative_division in PARSED_TITLE_07.children:
            assert putative_division.kind == "Division"


    def test_division_name_1(self):
        first_div = cast(Division, PARSED_TITLE_07.children[0])
        assert first_div.name == "Corporations"


    def test_division_names(self):
        names = [c.name for c in PARSED_TITLE_07.children]
        
        assert names == [
            'Corporations',
            'Associations',
            'Partnerships',
            'Trademarks and Business Names',
            'Trade Secrets',
            'Limited Liability Companies',
            'Corporations and Associations',
            'Corporations - Continued'
            ]

    def test_division_name_2(self):
        last_div = cast(Division, PARSED_TITLE_07.children[7])
        assert last_div.name == "Corporations - Continued"


    def test_correct_number_of_subdivisions(self):
        first_division = cast(Division, PARSED_TITLE_07.children[0])

        assert len(first_division.children) == 4
        for item in first_division.children:
            assert item.kind == "Subdivision"


    def test_subdivision_names(self):
        first_division = cast(Division, PARSED_TITLE_07.children[0])
        names = [c.name for c in first_division.children]
        
        assert names == ['Colorado Corporation Code', 'Nonprofit Corporations', 'Special Purpose Corporations', 'Religious and Benevolent Organizations']


    def test_subdiv_gets_div_name(self):
        first_div    = cast(Division, PARSED_TITLE_07.children[0])
        first_subdiv = cast(Subdivision, first_div.children[0])

        assert first_subdiv.division_name == first_div.name



class TestParseDivisions:
    def test_correct_number_of_divisions_1(self):
        assert len(PARSED_TITLE_16.children) == 8
        for putative_division in PARSED_TITLE_16.children:
            assert putative_division.kind == "Division"

    def test_correct_number_of_divisions_2(self):
        """Title 4 has no Divisions."""
        for putative_article in PARSED_TITLE_4.children:
            assert putative_article.kind == "Article"

    def test_first_division_retrieved(self):
        divs = PARSED_TITLE_16.children
        assert divs[0].name == "Code of Criminal Procedure"

    def test_second_division_retrieved(self):
        divs = PARSED_TITLE_16.children
        assert divs[1].name == "Uniform Mandatory Disposition of Detainers Act"

    @pytest.mark.skip
    def test_last_division_retrieved(self):
        divs = PARSED_TITLE_16.children
        assert divs[-1].name == "Offenders - Registration"

    # def we_can_get_a_div_editors_note(self):
    #     div_1 = PARSED_TITLE_16.children[0]

    #     assert (
    #         div_1.editors_note
    #         == "Articles 1 to 13 of this title (excluding articles 2.5, 2.7, 8.5, 11.3, 11.5, 11.7, 11.8, and 11.9) were numbered as articles 1 to 13 of chapter 39, C.R.S. 1963. The provisions of those articles were repealed and reenacted in 1972, resulting in the addition, relocation, and elimination of sections as well as subject matter. For amendments to those articles prior to 1972, consult the Colorado statutory research explanatory note beginning on page vii in the front of this volume. For a detailed comparison of those articles, see the comparative tables located in the back of the index."
    #     )
