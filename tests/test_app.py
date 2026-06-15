from types import SimpleNamespace

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.application.service import analyze_document, send_text_to_email
from app.main import app
from unittest.mock import patch

from app.worker.tasks import analyze_doc_task, send_message_to_email_task


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health(async_client):
        response = await async_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_analyze_document():
    with patch("app.application.service.extract_text_from_image") as mock_extract:
        mock_extract.return_value = "tesseract"

        result = analyze_document(b"fake image")

        assert result == {
        "status": "success",
        "text": "tesseract",
    }

        mock_extract.assert_called_once_with(b"fake image")

def test_send_text_to_email():
    with patch("app.application.service.send_email") as mock_smtp:

        result = send_text_to_email("text content")

        assert result == {
        "status": "success",
        "email_sent": True,
    }
        mock_smtp.assert_called_once_with("text content")

# tasks
def test_analyze_doc_task():
    with patch("app.worker.tasks.analyze_document") as mock_analyze:
        mock_analyze.return_value = {"status": "success", "text": "tesseract"}

        result = analyze_doc_task(b"fake image")

        assert result == "tesseract"

        mock_analyze.assert_called_once_with(b"fake image")

def test_send_message_to_email_task():
    with patch("app.worker.tasks.send_text_to_email") as mock_send:
        mock_send.return_value = {
        "status": "success",
        "email_sent": True,
    }
        result = send_message_to_email_task("text content")

        assert result == {
        "status": "success",
        "email_sent": True,
    }
        mock_send.assert_called_once_with("text content")

#endpoint
@pytest.mark.asyncio
async def test_send_message_to_email(async_client):
    with patch("app.api.router.send_message_to_email_task.delay") as mock_delay:
        mock_delay.return_value = SimpleNamespace(id="task-1")

        response = await async_client.post("/send_message_to_email/",
            json={"text": "text content"},
        )

        assert response.status_code == 200
        assert response.json() == {
            "status": "accepted",
            "task_id": "task-1",
            "message": "Сообщение принято в обработку",
    }

        mock_delay.assert_called_once_with("text content")

@pytest.mark.asyncio
async def test_analyze_doc(async_client):
    with patch("app.api.router.chain") as mock_chain:
        mock_chain.return_value.apply_async.return_value = SimpleNamespace(id="task-1")

        response = await async_client.post(
            "/analyze_doc/",
            files={"file": ("test.jpg", b"fake image", "image/jpeg")},
        )

        assert response.status_code == 200
        assert response.json() == {
            "status": "accepted",
            "task_id": "task-1",
            "message": "Файл принят в обработку",
        }

@pytest.mark.asyncio
async def test_send_message_to_email_negative(async_client):
    with patch("app.api.router.send_message_to_email_task.delay") as mock_delay:
        mock_delay.return_value = SimpleNamespace(id="task-1")

        response = await async_client.post("/send_message_to_email/",
            json={"wrong_field": "text"},
        )

        assert response.status_code == 422

        data = response.json()
        assert data["detail"] == "Ошибка валидации"
        assert "errors" in data
        assert data["errors"][0]["loc"] == ["body", "text"]
        assert data["errors"][0]["type"] == "missing"

        mock_delay.assert_not_called()

@pytest.mark.asyncio
async def test_analyze_doc_invalid_file(async_client):
    response = await async_client.post(
        "/analyze_doc/",
        files={
            "file": (
                "test.txt",
                b"text content",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Файл должен быть изображением"
    }