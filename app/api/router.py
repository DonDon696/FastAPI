from fastapi import APIRouter, UploadFile, Depends
from celery import chain

from app.api.dependencies import validate_image_file
from app.api.schemas import SendMessageToEmailRequest
from app.worker.tasks import send_message_to_email_task, analyze_doc_task

router = APIRouter()


@router.post("/analyze_doc/")
async def analyze_doc(file:UploadFile = Depends(validate_image_file)):

    image_bytes = await file.read()
    task = chain( analyze_doc_task.s(image_bytes),
                  send_message_to_email_task.s(),
                  ).apply_async()

    return {
        "status": "accepted",
        "task_id": task.id,
        "message": "Файл принят в обработку",
    }


@router.post("/send_message_to_email/")
async def send_message_to_email(payload: SendMessageToEmailRequest):
    task = send_message_to_email_task.delay(payload.text)

    return {
        "status": "accepted",
        "task_id": task.id,
        "message": "Сообщение принято в обработку",
    }


@router.get("/health")
def health():
    return {"status": "ok"}