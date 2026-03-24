import html
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from keyboards.inline import (
    BACK_TO_PLATFORMS_CALLBACK,
    DOWNLOAD_VIDEO_CALLBACK,
    PLATFORM_CALLBACK_PREFIX,
    link_actions_keyboard,
    platform_selection_keyboard,
    post_download_keyboard,
)
from services.downloader import DownloadedVideo, VideoDownloadError, download_video
from utils.config import settings
from utils.file_utils import cleanup_directory, format_bytes
from utils.link_validation import extract_url, validate_url_for_platform
from utils.messages import (
    GENERIC_DOWNLOAD_ERROR_TEXT,
    PLATFORM_SELECTION_TEXT,
    SEND_ERROR_TEXT,
    STATE_RESET_TEXT,
    VIDEO_CAPTION_FOOTER,
    invalid_link_text,
    link_request_text,
    loading_text,
    success_text,
    unknown_platform_text,
    video_too_large_text,
    wrong_platform_link_text,
)
from utils.states import DownloadStates

router = Router()
logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = {"tiktok", "youtube", "instagram"}


@router.callback_query(F.data == DOWNLOAD_VIDEO_CALLBACK)
async def choose_platform(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()

    if callback.message:
        await callback.message.answer(
            PLATFORM_SELECTION_TEXT,
            reply_markup=platform_selection_keyboard(),
        )


@router.callback_query(F.data.startswith(PLATFORM_CALLBACK_PREFIX))
async def platform_selected(callback: CallbackQuery, state: FSMContext) -> None:
    platform = callback.data.replace(PLATFORM_CALLBACK_PREFIX, "", 1)

    if platform not in SUPPORTED_PLATFORMS:
        await callback.answer()
        if callback.message:
            await callback.message.answer(
                unknown_platform_text(),
                reply_markup=platform_selection_keyboard(),
            )
        return

    await state.set_state(DownloadStates.awaiting_link)
    await state.update_data(platform=platform)
    await callback.answer()

    if callback.message:
        await callback.message.answer(
            link_request_text(platform),
            reply_markup=link_actions_keyboard(),
        )


@router.callback_query(F.data == BACK_TO_PLATFORMS_CALLBACK)
async def back_to_platforms(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()

    if callback.message:
        await callback.message.answer(
            PLATFORM_SELECTION_TEXT,
            reply_markup=platform_selection_keyboard(),
        )


@router.message(DownloadStates.awaiting_link)
async def process_video_link(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    platform = data.get("platform")

    if platform not in SUPPORTED_PLATFORMS:
        await state.clear()
        await message.answer(
            STATE_RESET_TEXT,
            reply_markup=platform_selection_keyboard(),
        )
        return

    url = extract_url(message.text or message.caption)
    if not url:
        await message.answer(
            invalid_link_text(platform),
            reply_markup=link_actions_keyboard(),
        )
        return

    if not validate_url_for_platform(platform, url):
        await message.answer(
            wrong_platform_link_text(platform),
            reply_markup=link_actions_keyboard(),
        )
        return

    status_message = await message.answer(loading_text(platform))

    downloaded_video: DownloadedVideo | None = None

    try:
        downloaded_video = await download_video(platform, url)

        safe_title = html.escape(downloaded_video.title[:100])
        caption = (
            f"🎬 <b>{safe_title}</b>\n"
            f"{VIDEO_CAPTION_FOOTER}"
        )

        await message.answer_video(
            video=FSInputFile(downloaded_video.file_path),
            caption=caption,
            supports_streaming=True,
        )
        await _delete_message_safely(status_message)
        await message.answer(
            success_text(platform),
            reply_markup=post_download_keyboard(),
        )
    except VideoDownloadError as error:
        logger.warning("Download error for %s: %s", platform, error.user_message)
        await status_message.edit_text(
            error.user_message,
            reply_markup=link_actions_keyboard(),
        )
    except TelegramBadRequest as error:
        logger.exception("Telegram send error: %s", error)
        error_text = str(error).lower()
        response_text = SEND_ERROR_TEXT
        if "too big" in error_text or "file is too big" in error_text:
            response_text = video_too_large_text(
                format_bytes(settings.max_video_size_bytes)
            )
        await status_message.edit_text(
            response_text,
            reply_markup=link_actions_keyboard(),
        )
    except Exception:
        logger.exception("Unexpected error while processing link")
        await status_message.edit_text(
            GENERIC_DOWNLOAD_ERROR_TEXT,
            reply_markup=link_actions_keyboard(),
        )
    finally:
        if downloaded_video is not None:
            cleanup_directory(downloaded_video.temp_dir)


async def _delete_message_safely(message: Message) -> None:
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.debug("Status message could not be deleted")
