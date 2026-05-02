import json, os

class Lang:
    def __init__(self):
        self.current = "en"
        self.data = {}
        self.load()

    def load(self):
        path = f"localization/{self.current}.json"
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def set(self, lang):
        self.current = lang
        self.load()

    def t(self, key):
        return self.data.get(key, key)

LANG = Lang()