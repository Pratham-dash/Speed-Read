from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(exc):
        return jsonify({"error": str(exc)}), 400

    @app.errorhandler(413)
    def too_large(_exc):
        return jsonify({"error": "Uploaded file exceeds maximum size"}), 413

    @app.errorhandler(Exception)
    def handle_exception(exc):
        if isinstance(exc, HTTPException):
            return jsonify({"error": exc.description}), exc.code
        app.logger.exception("Unhandled exception", exc_info=exc)
        return jsonify({"error": "Internal server error"}), 500
