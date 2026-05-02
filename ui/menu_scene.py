import tkinter as tk
from localization.lang import LANG

class MenuScene(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master)
        self.switch = switch

        self.title = tk.Label(self, font=("Arial", 18))
        self.title.pack(pady=20)

        self.btn_new = tk.Button(self, command=lambda: switch("game", True))
        self.btn_new.pack(pady=5)

        self.btn_continue = tk.Button(self, command=lambda: switch("game", False))
        self.btn_continue.pack(pady=5)

        # 🌍 кнопки мови
        lang_frame = tk.Frame(self)
        lang_frame.pack(pady=10)

        tk.Button(lang_frame, text="EN", command=lambda: self.set_lang("en")).pack(side="left")
        tk.Button(lang_frame, text="UA", command=lambda: self.set_lang("uk")).pack(side="left")

        self.update_text()

    def set_lang(self, lang):
        LANG.set(lang)
        self.update_text()

    def update_text(self):
        self.title.config(text=LANG.t("title"))
        self.btn_new.config(text=LANG.t("new_game"))
        self.btn_continue.config(text=LANG.t("continue"))