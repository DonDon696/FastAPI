from fastapi import File, HTTPException, UploadFile

async def validate_image_file(file: UploadFile = File(...)) -> UploadFile:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Файл должен быть изображением",
        )
    return file