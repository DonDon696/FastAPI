import io

from PIL import Image
import pytesseract

# Tesseract
def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang="eng+rus").strip()

    if not text:
        return "[Текст на изображении не найден]"

    return text