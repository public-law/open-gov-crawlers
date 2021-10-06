from dataclasses import dataclass

#
# Items for the Colorado Revised Statutes.
#


@dataclass
class Title:
    name: str
    number: str
    divisions: list


@dataclass
class Division:
    name: str
