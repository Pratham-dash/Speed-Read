import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    MAX_CONTENT_LENGTH: int = int(float(os.getenv("MAX_CONTENT_LENGTH_MB", "15")) * 1024 * 1024)
    DEFAULT_WPM: int = int(os.getenv("DEFAULT_WPM", "400"))
    MIN_WPM: int = int(os.getenv("MIN_WPM", "250"))
    MAX_WPM: int = int(os.getenv("MAX_WPM", "1000"))
    ALLOWED_ORIGINS: list[str] = tuple(_csv(os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")))
