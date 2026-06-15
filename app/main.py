from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.exceptions import ImageNotFoundError
from app.api.router import router
from app.api.handlers import image_not_found, validation_exception_handler
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="OCR & Email Service",
        lifespan=lifespan,
        )
    app.include_router(router)
    app.add_exception_handler(ImageNotFoundError, image_not_found)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    return app
app = create_app()




