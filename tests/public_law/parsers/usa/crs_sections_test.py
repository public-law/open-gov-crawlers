from scrapy.http.response.xml import XmlResponse

from public_law.parsers.usa.colorado.crs_sections import parse_sections
from public_law.test_util import *

# A Title with no Divisions.
TITLE_4 =  XmlResponse(body = fixture('usa', 'crs', "title04.xml"), url = "title04.xml", encoding = "utf-8")
TITLE_4_SECTIONS = parse_sections(TITLE_4, null_logger)

# A Title which uses Divisions.
TITLE_16 = XmlResponse(body = fixture('usa', 'crs', "title16.xml"), url = "title16.xml", encoding = "utf-8")
TITLE_16_SECTIONS  = parse_sections(TITLE_16, null_logger)
ARTICLE_1_SECTIONS = [s for s in TITLE_16_SECTIONS if s.article_number == "1"]

# A Title which uses Divisions.
TITLE_42 = XmlResponse(body = fixture('usa', 'crs', "title42.xml"), url = "title42.xml", encoding = "utf-8")
TITLE_42_SECTIONS = parse_sections(TITLE_42, null_logger)


# TODO: Title 4.


class TestSectionWithError:
    def test_name(self):
        section_42_4_2403 = [s for s in TITLE_42_SECTIONS if s.number == "42-4-2403"][0]
        assert section_42_4_2403.name == 'Applicability'


class TestSectionsGenerally:
    def test_article_has_correct_number_of_sections(self):
        """The parsing strategy is JSON lines. And so there isn't a
        direct API for this.
        """
        assert len(ARTICLE_1_SECTIONS) == 10


class TestParseFirstSection:
    SECTION = ARTICLE_1_SECTIONS[0]

    def test_number(self):
        assert self.SECTION.number == "16-1-101"

    def test_name(self):
        assert self.SECTION.name == "Short title"

    def test_article_number(self):
        assert self.SECTION.article_number == "1"

    def test_title_number(self):
        assert self.SECTION.title_number == "16"

    def test_text(self):
        assert self.SECTION.text == """<p>(1)</p>
<p>Articles 1 to 13 of this title shall be known and may be cited as the "Colorado Code of Criminal Procedure". Within those articles, the "Colorado Code of Criminal Procedure" is sometimes referred to as "this code".</p>
<p>(2)</p>
<p>The portion of any section, subsection, paragraph, or subparagraph contained in this code which precedes a list of examples, requirements, conditions, or other items may be referred to and cited as the "introductory portion" of such section, subsection, paragraph, or subparagraph.</p>"""



class TestParseLastSection:
    SECTION = ARTICLE_1_SECTIONS[-1]

    def test_article_number(self):
        assert self.SECTION.article_number == "1"

    def test_title_number(self):
        assert self.SECTION.title_number == "16"

    def test_number(self):
        assert self.SECTION.number == "16-1-110"

    def test_name(self):
        assert self.SECTION.name == "Regulation of showup identification procedures - definitions - repeal"



class TestParseSecondSection:
    SECTION = ARTICLE_1_SECTIONS[1]

    def test_article_number(self):
        assert self.SECTION.article_number == "1"

    def test_title_number(self):
        assert self.SECTION.title_number == "16"

    def test_number(self):
        assert self.SECTION.number == "16-1-102"

    def test_text(self):
        assert self.SECTION.text == '<p>The provisions of this code are intended to create, define, and protect rights, duties, and obligations as distinguished from matters wholly procedural. Except as specifically set forth in this code, the provisions of this code are not applicable to proceedings under the "Colorado Children\'s Code" or to violations of municipal charters or municipal ordinances.</p>'
