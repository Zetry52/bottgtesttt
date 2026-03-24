BOT_USERNAME = "@addownloaded_bot"

PLATFORM_LABELS = {
    "tiktok": "TikTok",
    "youtube": "YouTube",
    "instagram": "Instagram",
}

PLATFORM_EMOJIS = {
    "tiktok": "🎵",
    "youtube": "▶️",
    "instagram": "📸",
}

START_CAPTION = (
    "👋 <b>Здравствуйте!</b>\n\n"
    "Я помогу быстро и аккуратно скачать видео из <b>TikTok</b>, <b>YouTube</b> "
    "и <b>Instagram</b>.\n"
    "Нажмите кнопку ниже, выберите платформу и отправьте ссылку на ролик.\n\n"
    f"✨ Спасибо, что выбрали <b>{BOT_USERNAME}</b>."
)

HELP_TEXT = (
    "🆘 <b>Помощь</b>\n\n"
    "1. Нажмите <b>«📥 Скачать видео»</b>.\n"
    "2. Выберите нужную платформу.\n"
    "3. Отправьте ссылку на видео.\n\n"
    "Поддерживаются платформы:\n"
    "• TikTok\n"
    "• YouTube\n"
    "• Instagram\n\n"
    "Если ссылка неверная, видео недоступно, заблокировано или слишком большое для отправки в Telegram, "
    "бот подскажет это понятным сообщением.\n\n"
    "Команды:\n"
    "/start — главное меню\n"
    "/help — помощь"
)

PLATFORM_SELECTION_TEXT = (
    "🎯 <b>Выберите платформу</b>\n\n"
    "Откуда хотите скачать видео?\n"
    "После выбора я сразу попрошу ссылку и начну загрузку."
)

GENERIC_DOWNLOAD_ERROR_TEXT = (
    "❌ <b>Не удалось скачать видео</b>\n\n"
    "Попробуйте отправить ссылку ещё раз немного позже."
)

VIDEO_UNAVAILABLE_TEXT = (
    "⚠️ <b>Видео недоступно или заблокировано</b>\n\n"
    "Возможно, ролик удалён, приватный или его нельзя скачать."
)

INVALID_GENERIC_LINK_TEXT = (
    "🔗 <b>Проверьте правильность ссылки</b>\n\n"
    "Поддерживаются только корректные ссылки на TikTok, YouTube и Instagram."
)

SEND_ERROR_TEXT = (
    "❌ <b>Не удалось отправить видео</b>\n\n"
    "Возможно, файл слишком большой для Telegram или временно недоступен."
)

STATE_RESET_TEXT = (
    "⚠️ <b>Сессия сброшена</b>\n\n"
    "Пожалуйста, выберите платформу заново."
)

FALLBACK_TEXT = (
    "🙂 <b>Я готов помочь со скачиванием видео.</b>\n\n"
    "Нажмите <b>«📥 Скачать видео»</b>, выберите платформу и отправьте ссылку."
)

UNKNOWN_CALLBACK_TEXT = "⚠️ Кнопка устарела. Откройте нужный раздел снова."
VIDEO_CAPTION_FOOTER = f"📥 Скачано через <b>{BOT_USERNAME}</b>"


def platform_name(platform: str) -> str:
    label = PLATFORM_LABELS.get(platform, platform.title())
    emoji = PLATFORM_EMOJIS.get(platform, "📎")
    return f"{emoji} {label}"


def link_request_text(platform: str) -> str:
    return (
        f"📎 <b>Отправьте ссылку на видео из {platform_name(platform)}</b>\n\n"
        "Я приму ссылку, загружу ролик и сразу отправлю его сюда."
    )


def invalid_link_text(platform: str) -> str:
    return (
        f"🔗 <b>Пожалуйста, отправьте корректную ссылку на {platform_name(platform)}</b>\n\n"
        "Сейчас я жду именно ссылку на видео, а не обычный текст."
    )


def wrong_platform_link_text(platform: str) -> str:
    return (
        f"⚠️ <b>Похоже, это не ссылка на {platform_name(platform)}</b>\n\n"
        "Проверьте ссылку или вернитесь назад и выберите другую платформу."
    )


def loading_text(platform: str) -> str:
    return (
        f"⏳ <b>Загружаю видео из {platform_name(platform)}...</b>\n\n"
        "Обычно это занимает совсем немного времени."
    )


def success_text(platform: str) -> str:
    return (
        "✅ <b>Вот ваше видео!</b>\n\n"
        f"Спасибо за использование <b>{BOT_USERNAME}</b>.\n"
        f"📩 Можете прислать ещё ссылку на {platform_name(platform)} в любое время "
        "или выбрать другую платформу ниже."
    )


def video_too_large_text(limit: str) -> str:
    return (
        "📦 <b>Видео слишком большое для отправки в Telegram</b>\n\n"
        f"Пожалуйста, выберите ролик поменьше. Текущий лимит отправки: <b>{limit}</b>."
    )


def fallback_text() -> str:
    return FALLBACK_TEXT


def unknown_platform_text() -> str:
    return "⚠️ Не удалось определить платформу. Пожалуйста, выберите её заново."
