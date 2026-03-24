import asyncio
import logging
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from utils.config import settings
from utils.file_utils import format_bytes
from utils.messages import (
    GENERIC_DOWNLOAD_ERROR_TEXT,
    INVALID_GENERIC_LINK_TEXT,
    VIDEO_UNAVAILABLE_TEXT,
    video_too_large_text,
)

logger = logging.getLogger(__name__)

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}


@dataclass(slots=True)
class DownloadedVideo:
    file_path: Path
    temp_dir: Path
    title: str
    platform: str
    source_url: str
    file_size: int


class VideoDownloadError(Exception):
    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


async def download_video(platform: str, url: str) -> DownloadedVideo:
    platform = platform.lower()

    if platform == "tiktok":
        return await asyncio.to_thread(download_tiktok, url)
    if platform == "youtube":
        return await asyncio.to_thread(download_youtube, url)
    if platform == "instagram":
        return await asyncio.to_thread(download_instagram, url)

    raise VideoDownloadError(GENERIC_DOWNLOAD_ERROR_TEXT)


def download_tiktok(url: str) -> DownloadedVideo:
    logger.info("Downloading TikTok video: %s", url)
    options = {
        "format": "best[ext=mp4]/best",
    }
    return _download_with_yt_dlp("tiktok", url, options)


def download_youtube(url: str) -> DownloadedVideo:
    logger.info("Downloading YouTube video: %s", url)
    options = {
        "format": "best[ext=mp4][height<=720]/best[height<=720]/best[ext=mp4]/best",
    }
    return _download_with_yt_dlp("youtube", url, options)


def download_instagram(url: str) -> DownloadedVideo:
    logger.info("Downloading Instagram video: %s", url)
    options = {
        "format": "best[ext=mp4]/best",
    }
    return _download_with_yt_dlp("instagram", url, options)


def _download_with_yt_dlp(
    platform: str,
    url: str,
    platform_options: dict[str, Any],
) -> DownloadedVideo:
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=f"{platform}_", dir=settings.temp_dir))
    ydl_options = _build_ydl_options(temp_dir, platform_options)

    try:
        with YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)

        resolved_info = _resolve_info(info)
        file_path = _resolve_file_path(resolved_info, temp_dir)

        if file_path is None or not file_path.exists():
            raise VideoDownloadError(GENERIC_DOWNLOAD_ERROR_TEXT)

        file_size = file_path.stat().st_size
        if file_size > settings.max_video_size_bytes:
            raise VideoDownloadError(
                video_too_large_text(format_bytes(settings.max_video_size_bytes))
            )

        title = str(resolved_info.get("title") or "Видео")
        logger.info(
            "Downloaded %s video: %s (%s)",
            platform,
            file_path.name,
            format_bytes(file_size),
        )
        return DownloadedVideo(
            file_path=file_path,
            temp_dir=temp_dir,
            title=title,
            platform=platform,
            source_url=url,
            file_size=file_size,
        )
    except VideoDownloadError:
        cleanup_temp_dir(temp_dir)
        raise
    except DownloadError as error:
        logger.warning("yt-dlp download error for %s: %s", platform, error)
        cleanup_temp_dir(temp_dir)
        raise VideoDownloadError(_map_download_error(str(error))) from error
    except Exception as error:
        logger.exception("Unexpected downloader error for %s: %s", platform, error)
        cleanup_temp_dir(temp_dir)
        raise VideoDownloadError(GENERIC_DOWNLOAD_ERROR_TEXT) from error


def _build_ydl_options(
    temp_dir: Path,
    platform_options: dict[str, Any],
) -> dict[str, Any]:
    common_options: dict[str, Any] = {
        "outtmpl": str(temp_dir / "%(title).80s-%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "retries": 2,
        "fragment_retries": 2,
        "socket_timeout": 30,
        "overwrites": True,
        "nopart": True,
        "max_filesize": settings.max_video_size_bytes,
        "windowsfilenames": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/133.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    }
    common_options.update(platform_options)
    return common_options


def _resolve_info(info: dict[str, Any]) -> dict[str, Any]:
    if "entries" in info and info["entries"]:
        return info["entries"][0]
    return info


def _resolve_file_path(info: dict[str, Any], temp_dir: Path) -> Path | None:
    requested_downloads = info.get("requested_downloads") or []
    for item in requested_downloads:
        candidate = item.get("filepath") or item.get("_filename")
        if candidate:
            path = Path(candidate)
            if path.exists():
                return path

    for key in ("filepath", "_filename"):
        candidate = info.get(key)
        if candidate:
            path = Path(candidate)
            if path.exists():
                return path

    files = sorted(
        [file for file in temp_dir.iterdir() if file.is_file()],
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    )
    for file in files:
        if file.suffix.lower() in VIDEO_EXTENSIONS:
            return file
    return None


def _map_download_error(error_text: str) -> str:
    normalized = error_text.lower()

    if any(
        marker in normalized
        for marker in (
            "larger than max-filesize",
            "exceeds max_filesize",
            "file is larger than max-filesize",
        )
    ):
        return video_too_large_text(format_bytes(settings.max_video_size_bytes))

    if any(
        marker in normalized
        for marker in (
            "unsupported url",
            "not a valid url",
            "invalid url",
            "no video could be found",
        )
    ):
        return INVALID_GENERIC_LINK_TEXT

    if any(
        marker in normalized
        for marker in (
            "private",
            "login required",
            "sign in",
            "not available",
            "unavailable",
            "blocked",
            "forbidden",
            "404",
            "content isn't available",
            "requested content is not available",
        )
    ):
        return VIDEO_UNAVAILABLE_TEXT

    return GENERIC_DOWNLOAD_ERROR_TEXT


def cleanup_temp_dir(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
