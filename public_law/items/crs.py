from dataclasses import dataclass, field
import re
from typing import Optional

from public_law.text import NonemptyString, titleize, URL

#
# Items for the Colorado Revised Statutes.
#

@dataclass(frozen=True)
class Section:
    """A CRS Section.
    
    A typical section number looks like this:
        "16-1-101".

    It means:
        Title 16, Article 1, Maybe Part 1, Section 101.
    """
    name:           NonemptyString
    number:         NonemptyString
    text:           NonemptyString
    # Structure
    article_number: NonemptyString
    part_number:    Optional[NonemptyString]
    title_number:   NonemptyString
    kind:           str = 'Section'


@dataclass(frozen=True)
class Part:
    """CRS Part: a nonstructural namespace level.
    Used with Articles."""
    name: NonemptyString
    # Structure
    article_number: NonemptyString
    kind:           str = "Part"


@dataclass(frozen=True)
class Article:
    """A CRS Article."""
    name: NonemptyString
    number: NonemptyString
    # Structure
    title_number:  NonemptyString
    division_name: Optional[NonemptyString]
    kind:          str = "Article"


@dataclass
class Division:
    """CRS Division: a nonstructural namespace level.

    Used withing Titles. Some titles have Divisions, 
    others don't.
    """
    raw_name: NonemptyString
    name:     NonemptyString = field(init=False)
    # Structure
    articles:     list[Article]
    title_number: NonemptyString
    kind:         str = "Division"

    def validate(self):
        return re.match(r'[A-Z][A-Z]+', self.raw_name)
    
    def __post_init__(self):
        if not self.validate():
            raise ValueError(f"Invalid Division: {self.raw_name}")
        
        self.name = NonemptyString(titleize(self.raw_name))
        



@dataclass(frozen=True)
class Title:
    """A CRS Title."""
    name:       NonemptyString
    number:     NonemptyString
    # Structure
    children:   list[Division] | list[Article]
    source_url: URL
    kind:       str = "Title"
