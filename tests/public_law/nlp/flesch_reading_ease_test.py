# pyright: reportPrivateUsage=false
import pytest

from public_law.nlp.flesch_reading_ease import Difficulty, _score_to_difficulty


@pytest.mark.parametrize(
    "score, text",
    [
        (0, "Very difficult"),
        (30, "Difficult"),
        (50, "Fairly difficult"),
        (60, "Plain English"),
        (70, "Fairly easy"),
    ],
)
def it_converts_a_score(score: int, text: Difficulty):
    assert _score_to_difficulty(score) == text


def it_rounds_a_float_correctly():
    """
    The .5 should force it into the range of 70-80.
    """
    score = 69.5
    assert _score_to_difficulty(score) == "Fairly easy"
