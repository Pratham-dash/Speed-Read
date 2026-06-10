import re
from collections.abc import Iterable
from backend.services.orp_calculator import calculate_orp_index
from backend.services.timing_calculator import calculate_delay_ms
from backend.utils.constants import MAX_HEADING_WORDS, MIN_HEADING_WORDS


class TextProcessor:
    token_pattern = re.compile(r"\S+")

    @staticmethod
    def normalize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def is_heading_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        words = stripped.split()
        if not (MIN_HEADING_WORDS <= len(words) <= MAX_HEADING_WORDS):
            return False
        if stripped[-1] in ".,;:!?":
            return False
        if stripped.isupper():
            return True
        titlecase_ratio = sum(1 for w in words if w[:1].isupper()) / max(1, len(words))
        return titlecase_ratio >= 0.7

    def parse(self, text: str, wpm: int) -> list[dict]:
        words = []
        index = 0
        for line in self._iter_lines(text):
            heading = self.is_heading_line(line)
            for token in self.token_pattern.findall(line):
                words.append(
                    {
                        "index": index,
                        "word": token,
                        "orp_index": calculate_orp_index(token),
                        "delay_ms": calculate_delay_ms(token, wpm, heading),
                        "is_heading": heading,
                    }
                )
                index += 1
        return words

    def process(self, text: str, wpm: int) -> dict:
        words = self.parse(text, wpm)
        return {
            "wpm": wpm,
            "total_words": len(words),
            "estimated_read_seconds": round(sum(w["delay_ms"] for w in words) / 1000, 2),
            "words": words,
        }

    @staticmethod
    def _iter_lines(text: str) -> Iterable[str]:
        for line in text.splitlines() or [text]:
            cleaned = line.strip()
            if cleaned:
                yield cleaned
