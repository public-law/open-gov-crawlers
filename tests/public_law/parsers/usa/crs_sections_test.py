from scrapy.selector.unified import Selector

from public_law.test_util import fixture
from public_law.parsers.usa.colorado.crs import parse_sections



# A Title which uses Divisions.
TITLE_16 = Selector(text = fixture('usa', 'crs', "title16.xml"))
TITLE_16_SECTIONS = parse_sections(TITLE_16)
ARTICLE_1_SECTIONS = [s for s in TITLE_16_SECTIONS if s.article_number == "1"]



class TestSectionsGenerally:
    def test_article_has_correct_number_of_sections(self):
        """The parsing strategy is JSON lines. And so there isn't a
        direct API for this.
        """
        assert len(ARTICLE_1_SECTIONS) == 10



class TestParseFirstSection:
    def test_number(self):
        first_section  = ARTICLE_1_SECTIONS[0]
        assert first_section.number == "16-1-101"


    def test_name(self):
        first_section  = ARTICLE_1_SECTIONS[0]
        assert first_section.name == "Short title"



class TestParseLastSection:
    def test_number(self):
        last_section  = ARTICLE_1_SECTIONS[-1]

        assert last_section.number == "16-1-110"


    def test_name(self):
        last_section  = ARTICLE_1_SECTIONS[-1]

        assert last_section.name == "Regulation of showup identification procedures - definitions - repeal"
