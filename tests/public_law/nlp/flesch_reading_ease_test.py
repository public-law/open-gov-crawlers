# pyright: reportPrivateUsage=false

from public_law.nlp.flesch_reading_ease import _score_to_difficulty


class TestScoreToDifficulty:
    def it_handles_a_score_of_0(self):
        score = 0
        assert _score_to_difficulty(score) == "Very difficult"

    def it_handles_a_score_of_30(self):
        score = 30
        assert _score_to_difficulty(score) == "Difficult"

    def it_handles_a_score_of_50(self):
        score = 50
        assert _score_to_difficulty(score) == "Fairly difficult"

    def it_handles_a_score_of_60(self):
        score = 60
        assert _score_to_difficulty(score) == "Plain English"

    def it_handles_a_score_of_70(self):
        score = 70
        assert _score_to_difficulty(score) == "Fairly easy"

    def it_rounds_a_float_correctly(self):
        """
        The .5 should force it into the range of 70-80.
        """
        score = 69.5
        assert _score_to_difficulty(score) == "Fairly easy"
