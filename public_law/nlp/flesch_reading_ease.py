from textstat import analyzer

# Source: https://writingstudio.com/blog/flesch-reading-ease/
READING_SCORE_TO_DIFFICULTY = {
    range(90, 100): "Very easy",
    range(80, 90): "Easy",
    range(70, 80): "Fairly easy",
    range(60, 70): "Plain English",
    range(50, 60): "Fairly difficult",
    range(30, 50): "Difficult",
    range(0, 30): "Very difficult",
}


def reading_difficulty(text: str) -> str:
    """
    Calculate the reading difficulty of the text.
    """
    score = analyzer.flesch_reading_ease(text)
    return _score_to_difficulty(score)


def _score_to_difficulty(score: float) -> str:
    """
    Convert a reading score to a difficulty description.
    """
    int_score = round(score)

    for range_, difficulty in READING_SCORE_TO_DIFFICULTY.items():
        if int_score in range_:
            return difficulty
