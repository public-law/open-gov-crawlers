from dataclasses import dataclass

#
# Items for the Colorado Revised Statutes.
#


@dataclass(frozen=True)
class Title:
    name: str
    number: str
    divisions: list


@dataclass(frozen=True)
class Division:
    name: str
