import shutil
from pathlib import Path


def cleanup_directory(path: Path | str | None) -> None:
    if not path:
        return

    shutil.rmtree(Path(path), ignore_errors=True)


def format_bytes(size_in_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(size_in_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size_in_bytes} B"
