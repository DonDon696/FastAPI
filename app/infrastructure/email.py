import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings
# Структура письма
def build_email_message(text_content: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_user
    msg["To"] = settings.to_email
    msg["Subject"] = "Распознанный текст с изображения (Tesseract OCR)"

    body = f"Привет!\n\nВот текст, который удалось распознать:\n\n{text_content}"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    return msg

# Отправляет email через SMTP
def send_email(text_content: str) -> None:
    msg = build_email_message(text_content)

    with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(
            settings.smtp_user,
            settings.to_email,
            msg.as_string(),
        )