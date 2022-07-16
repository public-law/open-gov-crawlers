# pyright: reportPrivateUsage=false

from public_law.nlp.flesch_reading_ease import _score_to_difficulty


class TestScoreToDifficulty:
    def it_handles_a_score_of_0(self):
        score = 0
        assert _score_to_difficulty(score) == "Very difficult"
