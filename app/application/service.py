from app.infrastructure.email import send_email
from app.infrastructure.ocr import extract_text_from_image

# Получение изображения и вызывает ocr
def analyze_document(image_bytes: bytes) -> dict:
    text = extract_text_from_image(image_bytes)

    return {
        "status": "success",
        "text": text,
    }

# Получает готовый текст и вызывает email
def send_text_to_email(text_content: str) -> dict:
    send_email(text_content)

    return {
        "status": "success",
        "email_sent": True,
    }