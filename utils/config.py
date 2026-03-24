import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _resolve_assets_dir() -> Path:
    for folder_name in ("Assets", "assets"):
        candidate = BASE_DIR / folder_name
        if candidate.exists():
            return candidate
    return BASE_DIR / "Assets"


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    bot_username: str
    base_dir: Path
    assets_dir: Path
    logo_path: Path
    logs_dir: Path
    log_file: Path
    temp_dir: Path
    max_video_size_bytes: int


def _build_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError(
            "Переменная окружения BOT_TOKEN не найдена. "
            "Создайте файл .env на основе .env.example."
        )

    assets_dir = _resolve_assets_dir()
    return Settings(
        bot_token=bot_token,
        bot_username="@addownloaded_bot",
        base_dir=BASE_DIR,
        assets_dir=assets_dir,
        logo_path=assets_dir / "logo.png",
        logs_dir=BASE_DIR / "logs",
        log_file=BASE_DIR / "logs" / "bot.log",
        temp_dir=BASE_DIR / "temp",
        max_video_size_bytes=49 * 1024 * 1024,
    )


settings = _build_settings()
