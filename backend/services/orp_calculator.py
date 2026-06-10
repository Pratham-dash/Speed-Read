def calculate_orp_index(word: str) -> int:
    clean = "".join(ch for ch in word if ch.isalnum())
    length = len(clean)
    if length <= 1:
        return 0
    if length <= 5:
        return 1
    if length <= 9:
        return 2
    if length <= 13:
        return 3
    return min(length - 1, round(length * 0.35))
