from backend.services.orp_calculator import calculate_orp_index
from backend.services.text_processor import TextProcessor
from backend.services.timing_calculator import calculate_delay_ms


def test_orp_index_varies_with_length():
    assert calculate_orp_index("I") == 0
    assert calculate_orp_index("speed") == 1
    assert calculate_orp_index("reading") == 2
    assert calculate_orp_index("recognition") >= 3


def test_delay_respects_punctuation_and_heading():
    base = calculate_delay_ms("word", 400, is_heading=False)
    sentence = calculate_delay_ms("word.", 400, is_heading=False)
    heading = calculate_delay_ms("Chapter", 400, is_heading=True)

    assert sentence > base
    assert heading >= base * 5


def test_text_processor_detects_heading_and_tokens():
    processor = TextProcessor()
    result = processor.process("CHAPTER ONE\nThis is sample text.", 400)

    assert result["total_words"] == 6
    assert result["words"][0]["is_heading"] is True
    assert result["words"][2]["is_heading"] is False
