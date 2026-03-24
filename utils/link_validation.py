import re

URL_PATTERN = re.compile(r"(https?://[^\s]+)", re.IGNORECASE)

YOUTUBE_PATTERN = re.compile(
    r"^https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)",
    re.IGNORECASE,
)
TIKTOK_PATTERN = re.compile(
    r"^https?://(?:www\.)?(?:(?:vm|vt|m)\.tiktok\.com/|tiktok\.com/)",
    re.IGNORECASE,
)
INSTAGRAM_PATTERN = re.compile(
    r"^https?://(?:www\.)?(?:instagram\.com|instagr\.am)/(?:reel|p|tv)/",
    re.IGNORECASE,
)


def extract_url(text: str | None) -> str | None:
    if not text:
        return None

    match = URL_PATTERN.search(text.strip())
    if not match:
        return None

    return match.group(1).rstrip(".,)")


def validate_youtube_url(url: str) -> bool:
    return bool(YOUTUBE_PATTERN.match(url.strip()))


def validate_tiktok_url(url: str) -> bool:
    return bool(TIKTOK_PATTERN.match(url.strip()))


def validate_instagram_url(url: str) -> bool:
    return bool(INSTAGRAM_PATTERN.match(url.strip()))


def validate_url_for_platform(platform: str, url: str) -> bool:
    validators = {
        "youtube": validate_youtube_url,
        "tiktok": validate_tiktok_url,
        "instagram": validate_instagram_url,
    }
    validator = validators.get(platform.lower())
    if validator is None:
        return False
    return validator(url)
