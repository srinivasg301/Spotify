from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from app.routers.artist_router import router as artist_router
from app.routers.song_router import admin_router, router as song_router

app = FastAPI(title=settings.app_name, debug=settings.debug, version="1.0.0")

app.include_router(artist_router)
app.include_router(song_router)
app.include_router(admin_router)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", response_model=dict)
async def root() -> dict:
    return {"success": True, "data": {"message": "Spotify-like backend is running"}}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "data": None, "message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"success": False, "data": None, "message": "Validation error", "errors": exc.errors()},
    )
