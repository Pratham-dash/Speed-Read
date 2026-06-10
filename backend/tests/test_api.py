import io
from backend.app import create_app


def _client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health():
    client = _client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_process_text_validation():
    client = _client()
    response = client.post("/api/process-text", json={"text": "", "wpm": 300})
    assert response.status_code == 400


def test_process_txt_upload():
    client = _client()
    data = {
        "file": (io.BytesIO(b"CHAPTER 1\nHello world"), "sample.txt"),
        "wpm": "350",
    }
    response = client.post("/api/process-pdf", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    body = response.get_json()
    assert body["total_words"] == 4
