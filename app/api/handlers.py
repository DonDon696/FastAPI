from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.api.exceptions import ImageNotFoundError

async def image_not_found(request: Request, exception: ImageNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Image not found"}
    )

async def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Ошибка валидации", "errors": exception.errors()},
    )