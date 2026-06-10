import logging
import re

logger = logging.getLogger(__name__)

try:
    from docling.document_converter import DocumentConverter
except Exception:  # pragma: no cover - optional dependency in tests
    DocumentConverter = None


class PDFProcessor:
    chapter_start_pattern = re.compile(r"^(chapter\s+\d+|\d+\.|part\s+\w+)", re.IGNORECASE)

    def extract_main_content(self, path: str) -> str:
        if DocumentConverter is None:
            raise RuntimeError("docling is not available")

        converter = DocumentConverter()
        result = converter.convert(path)
        text = self._extract_text(result)
        return self._clean_extracted_text(text)

    def _extract_text(self, result) -> str:
        if hasattr(result, "document") and hasattr(result.document, "export_to_markdown"):
            return result.document.export_to_markdown()
        if hasattr(result, "document") and hasattr(result.document, "text"):
            return str(result.document.text)
        return str(result)

    def _clean_extracted_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]

        started = False
        filtered: list[str] = []
        for line in lines:
            lowered = line.lower()
            if not started and self.chapter_start_pattern.search(lowered):
                started = True
            if not started:
                continue
            if self._is_header_footer_or_footnote(line):
                continue
            filtered.append(line)

        return "\n".join(filtered).strip()

    @staticmethod
    def _is_header_footer_or_footnote(line: str) -> bool:
        if re.fullmatch(r"\d+", line):
            return True
        if re.match(r"^\[?\d+\]?\s", line):
            return True
        if len(line) < 4:
            return True
        if line.count("|") >= 2:
            return True
        return False
