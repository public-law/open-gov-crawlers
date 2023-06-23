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
    FIRST = ARTICLE_1_SECTIONS[0]

    def test_number(self):
        assert self.FIRST.number == "16-1-101"

    def test_name(self):
        assert self.FIRST.name == "Short title"


class TestParseSecondSection:
    SECOND = ARTICLE_1_SECTIONS[1]

    def test_number(self):
        assert self.SECOND.number == "16-1-102"

    def test_text(self):
        assert self.SECOND.text == '<p>The provisions of this code are intended to create, define, and protect rights, duties, and obligations as distinguished from matters wholly procedural. Except as specifically set forth in this code, the provisions of this code are not applicable to proceedings under the "Colorado Children\'s Code" or to violations of municipal charters or municipal ordinances.</p>'


class TestParseLastSection:
    LAST = ARTICLE_1_SECTIONS[-1]

    def test_number(self):
        assert self.LAST.number == "16-1-110"

    def test_name(self):
        assert self.LAST.name == "Regulation of showup identification procedures - definitions - repeal"
