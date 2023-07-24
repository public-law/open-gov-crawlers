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
    title_number:     NonemptyString
    division_name:    Optional[NonemptyString]
    subdivision_name: Optional[NonemptyString]
    kind:             str = "Article"


@dataclass
class Subdivision:
    """CRS Subdivision: a nonstructural namespace level.

    Used within Divisions. Some Divisions have Subdivisions, 
    others don't. All Subdivisions' raw names are title-case.
    """
    raw_name: NonemptyString
    name:     NonemptyString = field(init=False)
    # Structure
    articles:      list[Article]
    division_name: NonemptyString
    title_number:  NonemptyString
    kind:         str = "Subdivision"

    def validate(self):
        return self.is_valid_raw_name(self.raw_name)
    
    def __post_init__(self):
        if not self.validate():
            raise ValueError(f"Invalid Subdivision: {self.raw_name}")
        
        self.name = self.name_from_raw(self.raw_name)

    @staticmethod
    def is_valid_raw_name(raw_name: str | None) -> bool:
        return re.match(r'[A-Z][a-z]+', raw_name or '') is not None

    @staticmethod
    def name_from_raw(raw_name: str) -> NonemptyString:
        return NonemptyString(titleize(raw_name))




@dataclass
class Division:
    """CRS Division: a nonstructural namespace level.

    Used within Titles. Some titles have Divisions, 
    others don't. All Divisions' raw names are upper case.
    """
    raw_name: NonemptyString
    name:     NonemptyString = field(init=False)
    # Structure
    children:     list[Subdivision] | list[Article]
    title_number: NonemptyString
    kind:         str = "Division"

    def validate(self):
        return self.is_valid_raw_name(self.raw_name)
    
    def __post_init__(self):
        if not self.validate():
            raise ValueError(f"Invalid Division: {self.raw_name}")
        
        self.name = self.name_from_raw(self.raw_name)

    @staticmethod
    def is_valid_raw_name(raw_name: str|None) -> bool:
        return re.match(r'[A-Z][A-Z]+', raw_name or '') is not None
    
    @staticmethod
    def name_from_raw(raw_name: str) -> NonemptyString:
        return NonemptyString(titleize(raw_name))

        

@dataclass(frozen=True)
class Title:
    """A CRS Title."""
    name:       NonemptyString
    number:     NonemptyString
    # Structure
    children:   list[Division] | list[Article]
    source_url: URL
    kind:       str = "Title"
