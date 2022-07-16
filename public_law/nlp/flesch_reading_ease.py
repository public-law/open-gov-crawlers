from typing import Any, Literal, TypeAlias
from textstat import analyzer

# Source: https://writingstudio.com/blog/flesch-reading-ease/

Difficulty: TypeAlias = Literal[
    "Very easy",
    "Easy",
    "Fairly easy",
    "Plain English",
    "Fairly difficult",
    "Difficult",
    "Very difficult",
]


class RangeDict(dict[range, Difficulty]):
    """
    A dictionary that maps a range of scores to a difficulty.
    """

    def __getitem__(self, item: Any) -> Difficulty:
        """
        Iterate over the intervals. If the argument is in that interval
        return its associated value. If not in any interval, raise KeyError.
        """
        int_item = round(item)

        for key in self.keys():
            if int_item in key:
                return super().__getitem__(key)

        raise KeyError(item)


READING_SCORE_TO_DIFFICULTY = RangeDict(
    {
        range(90, 100): "Very easy",
        range(80, 90): "Easy",
        range(70, 80): "Fairly easy",
        range(60, 70): "Plain English",
        range(50, 60): "Fairly difficult",
        range(30, 50): "Difficult",
        range(0, 30): "Very difficult",
    }
)


def reading_difficulty(text: str) -> Difficulty:
    """
    Calculate the reading difficulty of the text.
    """
    score = analyzer.flesch_reading_ease(text)
    return _score_to_difficulty(score)


def _score_to_difficulty(score: float) -> Difficulty:
    """
    Convert a reading score to a difficulty description.
    """
    return READING_SCORE_TO_DIFFICULTY[score]
