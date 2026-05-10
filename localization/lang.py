import json
import os

LANG = "en"

BASE_DIR = os.path.dirname(__file__)

with open(
    os.path.join(BASE_DIR, "en.json"),
    encoding="utf-8"
) as f:
    EN = json.load(f)

with open(
    os.path.join(BASE_DIR, "uk.json"),
    encoding="utf-8"
) as f:
    UK = json.load(f)

TEXT = {
    "en": EN,
    "ua": UK
}


def t(key):

    return TEXT.get(LANG, {}).get(key, key)


def set_lang(lang):

    global LANG

    LANG = lang


def switch_lang():

    global LANG

    LANG = "ua" if LANG == "en" else "en"


def get_lang():

    return LANG