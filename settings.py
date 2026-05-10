import json
import os

from localization.lang import set_lang

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "language": "en",
    "volume": 0.5,
    "mute": False,
    "difficulty": "normal",
    "fullscreen": False,
    "animations": True,
    "show_fps": False,

    "custom_music": "",
    "custom_build_sound": "",
    "custom_click_sound": "",
    "custom_event_sound": ""
}

# cached settings (IMPORTANT FIX)
_settings_cache = None


# =====================
# INTERNAL LOAD
# =====================

def _load_raw():
    if not os.path.exists(SETTINGS_FILE):
        return None

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# =====================
# LOAD SETTINGS (SAFE)
# =====================

def load_settings():
    global _settings_cache

    if _settings_cache is not None:
        return _settings_cache

    data = _load_raw()

    if not data:
        data = DEFAULT_SETTINGS.copy()
        save_settings(data)

    # fill missing keys
    for k, v in DEFAULT_SETTINGS.items():
        if k not in data:
            data[k] = v

    _settings_cache = data
    return data


# =====================
# APPLY SETTINGS (IMPORTANT FIX FOR TRANSLATION)
# =====================

def apply_settings():
    """
    Call this ONCE at startup or when user changes settings.
    This is where translation is applied.
    """

    settings = load_settings()

    lang = settings.get("language", "en")

    # THIS is the ONLY correct place for translation update
    set_lang(lang)


# =====================
# SAVE SETTINGS
# =====================

def save_settings(settings):
    global _settings_cache

    _settings_cache = settings

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


# =====================
# GET
# =====================

def get_setting(key):
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))


# =====================
# SET
# =====================

def set_setting(key, value):
    settings = load_settings()
    settings[key] = value

    save_settings(settings)


# =====================
# RESET
# =====================

def reset_settings():
    global _settings_cache

    _settings_cache = DEFAULT_SETTINGS.copy()
    save_settings(_settings_cache)
    apply_settings()


# =====================
# AUDIO PATH HELPERS
# =====================

def get_music_path():
    settings = load_settings()

    path = settings.get("custom_music", "")
    if path and os.path.exists(path):
        return path

    return "assets/music/game.mp3"


def get_sound_path(sound_name):
    settings = load_settings()

    mapping = {
        "build": settings.get("custom_build_sound", ""),
        "click": settings.get("custom_click_sound", ""),
        "event": settings.get("custom_event_sound", "")
    }

    custom = mapping.get(sound_name, "")

    if custom and os.path.exists(custom):
        return custom

    return f"assets/sounds/{sound_name}.wav"