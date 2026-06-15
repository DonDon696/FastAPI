from pydantic import BaseModel


class SendMessageToEmailRequest(BaseModel):
    text: str