from aiogram import Router

from .download import router as download_router
from .fallbacks import router as fallback_router
from .start import router as start_router


def get_routers() -> list[Router]:
    return [start_router, download_router, fallback_router]
