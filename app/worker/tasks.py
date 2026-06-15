from app.application.service import send_text_to_email, analyze_document
from app.infrastructure.celery_app import celery_app

# задача фоновой обработки изображения
@celery_app.task
def analyze_doc_task(image_bytes: bytes):
    result = analyze_document(image_bytes)
    return result["text"]

# Фоновая задача для отправки письма
@celery_app.task
def send_message_to_email_task(text_content: str):
    return send_text_to_email(text_content)

