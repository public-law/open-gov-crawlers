from dataclasses import dataclass

from public_law.metadata import Metadata
from public_law.text import NonemptyString


class ParseException(Exception):
    pass


@dataclass(frozen=True)
class GlossaryEntry:
    """Represents one term and its definition in a particular Glossary"""

    phrase: NonemptyString
    definition: NonemptyString


@dataclass(frozen=True)
class GlossaryParseResult:
    """All the info about a glossary"""

    metadata: Metadata
    entries: list[GlossaryEntry]

    def __iter__(self):
        """Iterate over the entries in this glossary source.
        This customizes the produced dict to properly process the
        metadata.

        TODO: Figure out a way to convert this to a dict without the
        custom __iter__.
        """

        new_dict = {
            "metadata": dict(self.metadata),
            "entries": self.entries,
        }
        return iter(new_dict.items())
