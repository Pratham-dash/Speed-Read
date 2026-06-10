import os
from backend.utils.constants import ALLOWED_FILE_EXTENSIONS


def validate_wpm(wpm: int, min_wpm: int, max_wpm: int) -> int:
    try:
        value = int(wpm)
    except (TypeError, ValueError):
        raise ValueError("wpm must be an integer")

    if value < min_wpm or value > max_wpm:
        raise ValueError(f"wpm must be between {min_wpm} and {max_wpm}")

    return value


def validate_upload_filename(filename: str) -> str:
    if not filename:
        raise ValueError("Missing file name")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise ValueError("Unsupported file type. Allowed: pdf, txt")
    return ext


def secure_temp_name(filename: str) -> str:
    return os.path.basename(filename)
