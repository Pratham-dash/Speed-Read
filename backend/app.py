from flask import Flask
from flask_cors import CORS

from backend.api.error_handlers import register_error_handlers
from backend.api.routes import api_bp
from backend.config import Config
from backend.utils.logger import configure_logging


def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)
    cfg = Config()
    app.config.from_mapping(
        SECRET_KEY=cfg.SECRET_KEY,
        MAX_CONTENT_LENGTH=cfg.MAX_CONTENT_LENGTH,
        DEFAULT_WPM=cfg.DEFAULT_WPM,
        MIN_WPM=cfg.MIN_WPM,
        MAX_WPM=cfg.MAX_WPM,
    )

    CORS(app, resources={r"/api/*": {"origins": list(cfg.ALLOWED_ORIGINS)}})

    app.register_blueprint(api_bp)
    register_error_handlers(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
