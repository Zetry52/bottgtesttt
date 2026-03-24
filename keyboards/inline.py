from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

DOWNLOAD_VIDEO_CALLBACK = "download_video"
GO_HOME_CALLBACK = "go_home"
BACK_TO_PLATFORMS_CALLBACK = "back_to_platforms"
PLATFORM_CALLBACK_PREFIX = "platform:"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📥 Скачать видео", callback_data=DOWNLOAD_VIDEO_CALLBACK)
    builder.adjust(1)
    return builder.as_markup()


def help_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📥 Скачать видео", callback_data=DOWNLOAD_VIDEO_CALLBACK)
    builder.button(text="🏠 В главное меню", callback_data=GO_HOME_CALLBACK)
    builder.adjust(1)
    return builder.as_markup()


def platform_selection_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎵 TikTok", callback_data=f"{PLATFORM_CALLBACK_PREFIX}tiktok")
    builder.button(text="▶️ YouTube", callback_data=f"{PLATFORM_CALLBACK_PREFIX}youtube")
    builder.button(text="📸 Instagram", callback_data=f"{PLATFORM_CALLBACK_PREFIX}instagram")
    builder.button(text="🏠 В главное меню", callback_data=GO_HOME_CALLBACK)
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def link_actions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data=BACK_TO_PLATFORMS_CALLBACK)
    builder.button(text="🏠 В главное меню", callback_data=GO_HOME_CALLBACK)
    builder.adjust(1, 1)
    return builder.as_markup()


def post_download_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data=BACK_TO_PLATFORMS_CALLBACK)
    builder.button(text="🏠 В главное меню", callback_data=GO_HOME_CALLBACK)
    builder.adjust(1, 1)
    return builder.as_markup()
