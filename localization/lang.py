import json

LANG = "en"
DATA = {}

LISTENERS = []


def load_lang(lang):
    global DATA, LANG
    LANG = lang

    with open(f"localization/{lang}.json", "r", encoding="utf-8") as f:
        DATA = json.load(f)

    notify_listeners()


def t(key):
    return DATA.get(key, key)


def get_lang():
    return LANG


def set_lang(lang):
    load_lang(lang)


# =====================
# LIVE SYSTEM
# =====================

def register_listener(callback):
    if callback not in LISTENERS:
        LISTENERS.append(callback)


def unregister_listener(callback):
    if callback in LISTENERS:
        LISTENERS.remove(callback)


def notify_listeners():
    for cb in LISTENERS:
        try:
            cb()
        except:
            pass