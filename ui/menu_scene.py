import tkinter as tk
from localization.lang import LANG

class MenuScene(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master)
        self.switch = switch

        # ===== TITLE =====
        self.title = tk.Label(self, font=("Arial", 18))
        self.title.pack(pady=20)

        # ===== DIFFICULTY =====
        self.diff_var = tk.StringVar(value="normal")

        diff_frame = tk.Frame(self)
        diff_frame.pack(pady=10)

        self.diff_label = tk.Label(diff_frame)
        self.diff_label.pack()

        self.rb_easy = tk.Radiobutton(
            diff_frame,
            variable=self.diff_var,
            value="easy"
        )
        self.rb_easy.pack(anchor="w")

        self.rb_normal = tk.Radiobutton(
            diff_frame,
            variable=self.diff_var,
            value="normal"
        )
        self.rb_normal.pack(anchor="w")

        self.rb_hard = tk.Radiobutton(
            diff_frame,
            variable=self.diff_var,
            value="hard"
        )
        self.rb_hard.pack(anchor="w")

        # ===== BUTTONS =====
        self.btn_new = tk.Button(
            self,
            command=lambda: self.switch("game", True, self.diff_var.get())
        )
        self.btn_new.pack(pady=5)

        self.btn_continue = tk.Button(
            self,
            command=lambda: self.switch("game", False, self.diff_var.get())
        )
        self.btn_continue.pack(pady=5)

        # ===== LANGUAGE =====
        lang_frame = tk.Frame(self)
        lang_frame.pack(pady=10)

        tk.Button(lang_frame, text="EN", command=lambda: self.set_lang("en")).pack(side="left")
        tk.Button(lang_frame, text="UA", command=lambda: self.set_lang("uk")).pack(side="left")

        self.update_text()

    # ===== LANGUAGE SWITCH =====
    def set_lang(self, lang):
        LANG.set(lang)
        self.update_text()

        if hasattr(self.master, "game"):
            self.master.game.update_texts()

    # ===== UPDATE TEXT =====
    def update_text(self):
        t = LANG.t

        self.title.config(text=t("title"))
        self.btn_new.config(text=t("new_game"))
        self.btn_continue.config(text=t("continue"))

        self.diff_label.config(text=t("difficulty"))

        self.rb_easy.config(text="🟢 " + t("easy"))
        self.rb_normal.config(text="🟡 " + t("normal"))
        self.rb_hard.config(text="🔴 " + t("hard"))