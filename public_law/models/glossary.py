from dataclasses import dataclass
from functools import cached_property
from typing import Iterable

from ..metadata import Metadata
from ..text import NonemptyString, Sentence
from ..nlp.flesch_reading_ease import reading_difficulty


@dataclass(frozen=True)
class GlossaryEntry:
    """Represents one term and its definition in a particular Glossary"""

    phrase: NonemptyString
    definition: Sentence


@dataclass(frozen=True)
class GlossaryParseResult:
    """All the info about a glossary"""

    metadata: Metadata
    entries: Iterable[GlossaryEntry]

    @cached_property
    def reading_ease(self):
        """
        The readability index for this glossary.
        """
        return reading_difficulty(self.__definition_corpus())

    def __definition_corpus(self) -> NonemptyString:
        """
        All the definition text for this glossary.
        """
        return NonemptyString("  ".join(entry.definition for entry in self.entries))

    def __iter__(self):
        """Iterate over the entries in this glossary source.
        This customizes the produced dict to properly process the
        metadata.

        TODO: Figure out a way to convert this to a dict without the
        custom __iter__.
        """
        new_dict = {
            "metadata": dict(self.metadata),
            "entries": tuple(self.entries),
        }
        return iter(new_dict.items())

    def __repr__(self) -> str:
        return f"GlossaryParseResult(reading_ease={self.reading_ease})"
