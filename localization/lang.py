import json
import os
import locale


class Lang:
    def __init__(self):
        self.current = self.detect_system_lang()
        self.data = {}
        self.load()

    # =====================
    # AUTO DETECT
    # =====================
    def detect_system_lang(self):
        sys_lang = locale.getdefaultlocale()[0]

        if sys_lang:
            if sys_lang.startswith("uk"):
                return "uk"
            if sys_lang.startswith("ru"):
                return "ua"
        return "en"

    # =====================
    # LOAD JSON
    # =====================
    def load(self):
        path = f"localization/{self.current}.json"

        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    # =====================
    # CHANGE LANGUAGE
    # =====================
    def set(self, lang):
        self.current = lang
        self.load()

    # =====================
    # GET TEXT
    # =====================
    def t(self, key):
        return self.data.get(key, key)


# 🔥 GLOBAL INSTANCE (ВАЖЛИВО)
LANG = Lang()