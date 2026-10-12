# config_loader.py
# Reads settings.cfg. Hand-rolled in 2013; modernised 2025.
# Note: get_setting() is a thin wrapper around dict.get() — kept for backward compatibility.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Parse *path* (defaults to settings.cfg) and return a dict of known keys."""
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Unknown keys are silently dropped — a typo in the cfg will never surface.
            if key in KNOWN_KEYS:
                settings[key] = value   # everything stays a string; callers convert
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return settings[key] as an int, or *fallback* if the key is absent or not an int."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return settings[key], or *fallback* if the key is absent. (Thin wrapper over dict.get.)"""
    return settings.get(key, fallback)
