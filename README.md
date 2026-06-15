# OCR & Email Service

Сервис на FastAPI для распознавания текста на изображениях и отправки результата на email.

## Стек

- FastAPI
- Celery
- Redis
- Tesseract OCR
- Docker / Docker Compose
- Pytest

## Запуск через Docker

```bash
docker compose up --build
```

## Запуск локально

```bash
uvicorn app.main:app --reload
```

## Запуск Celery

```bash
celery -A app.infrastructure.celery_app.celery_app worker --loglevel=info
```

## Тесты

```bash
pytest --cov=app
```

## Эндпоинты

### POST /analyze_doc/

Принимает изображение, распознаёт текст и отправляет результат на email через Celery.

### POST /send_message_to_email/

Отправляет переданный текст на email через Celery.

### GET /health

Проверка состояния сервиса.
