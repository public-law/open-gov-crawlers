import dataclasses
from dataclasses import dataclass
from typing import Any, Optional

from public_law.shared.models.metadata import Metadata
from public_law.shared.utils.text import NonemptyString, URI


@dataclass(frozen=True)
class StatuteEntry:
    """Represents a single statute section or provision."""
    
    # Core fields
    title: NonemptyString              # e.g., "Title 16" 
    chapter: Optional[NonemptyString]  # e.g., "Chapter 3"
    section: NonemptyString            # e.g., "Section 16-3-101"
    text: NonemptyString               # Full text of the statute
    citation: NonemptyString           # Official citation
    
    # Metadata
    url: URI                           # Source URL
    effective_date: Optional[str]      # When the statute became effective
    last_updated: Optional[str]        # Last modification date
    
    # Hierarchical structure
    part: Optional[NonemptyString]     # Some states use parts
    article: Optional[NonemptyString]  # Some states use articles
    subsection: Optional[NonemptyString] # Subsection identifier
    
    kind: str = "StatuteEntry"

    def asdict(self):
        return dataclasses.asdict(self)


@dataclass(frozen=True)
class StatuteParseResult:
    """Collection of all statute entries from a state."""
    
    metadata: Metadata
    entries: tuple[StatuteEntry, ...]
    
    def asdict(self):
        return {
            "metadata": self.metadata.asdict(),
            "entries": [entry.asdict() for entry in self.entries],
        }

    def __contains__(self, item: Any) -> bool:
        return self.asdict().__contains__(item)

    def __getitem__(self, item: Any) -> Any:
        return self.asdict().__getitem__(item)

    def __eq__(self, __t: Any):
        return self.asdict().__eq__(__t)

    def __ne__(self, __t: Any):
        return self.asdict().__ne__(__t)

    def __iter__(self):
        return self.asdict().__iter__()

    def __len__(self):
        return len(self.entries)