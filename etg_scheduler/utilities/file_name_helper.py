import re
from datetime import datetime


def safe_file_part(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = normalized.strip("_")
    return normalized or "scenario"


def timestamp_suffix(moment: datetime | None = None) -> str:
    selected = moment or datetime.now()
    return selected.strftime("%Y%m%d_%H%M%S")
