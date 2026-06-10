import os
import tempfile
from flask import Blueprint, current_app, jsonify, request
from backend.api.validators import secure_temp_name, validate_upload_filename, validate_wpm
from backend.services.pdf_processor import PDFProcessor
from backend.services.text_processor import TextProcessor

api_bp = Blueprint("api", __name__)
_processor = TextProcessor()
_pdf_processor = PDFProcessor()
_last_stats: dict = {"total_words": 0, "estimated_read_seconds": 0, "source": "none"}


@api_bp.get("/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@api_bp.post("/api/process-text")
def process_text() -> tuple:
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        raise ValueError("text is required")

    wpm = validate_wpm(payload.get("wpm", current_app.config["DEFAULT_WPM"]), current_app.config["MIN_WPM"], current_app.config["MAX_WPM"])
    result = _processor.process(text, wpm)
    _last_stats.update({"total_words": result["total_words"], "estimated_read_seconds": result["estimated_read_seconds"], "source": "text"})
    return jsonify(result), 200


@api_bp.post("/api/process-pdf")
def process_pdf() -> tuple:
    if "file" not in request.files:
        raise ValueError("file is required")

    upload = request.files["file"]
    extension = validate_upload_filename(upload.filename)
    wpm = validate_wpm(request.form.get("wpm", current_app.config["DEFAULT_WPM"]), current_app.config["MIN_WPM"], current_app.config["MAX_WPM"])

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as tmp_file:
        upload.save(tmp_file.name)
        temp_path = tmp_file.name

    try:
        if extension == "txt":
            with open(temp_path, "r", encoding="utf-8", errors="ignore") as txt_file:
                extracted = txt_file.read()
        else:
            extracted = _pdf_processor.extract_main_content(temp_path)

        result = _processor.process(extracted, wpm)
        _last_stats.update({"total_words": result["total_words"], "estimated_read_seconds": result["estimated_read_seconds"], "source": extension})
        return jsonify(result), 200
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@api_bp.get("/api/get-stats")
def get_stats() -> tuple:
    return jsonify(_last_stats), 200
