from backend.utils.constants import PHRASE_PUNCTUATION, SENTENCE_PUNCTUATION


def _length_multiplier(word: str) -> float:
    chars = len("".join(ch for ch in word if ch.isalnum()))
    if chars <= 3:
        return 0.9
    if chars <= 6:
        return 1.0
    if chars <= 9:
        return 1.2
    return 1.4


def calculate_delay_ms(word: str, wpm: int, is_heading: bool = False) -> int:
    base_ms = max(1, int(60000 / max(1, wpm)))
    delay = int(base_ms * _length_multiplier(word))

    if word and word[-1] in SENTENCE_PUNCTUATION:
        delay += base_ms * 2
    elif word and word[-1] in PHRASE_PUNCTUATION:
        delay += base_ms

    if is_heading:
        delay *= 5

    return delay
