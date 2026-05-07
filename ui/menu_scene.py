import tkinter as tk
from localization.lang import LANG


class MenuScene(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master)
        self.master = master
        self.switch = switch

        self.configure(bg="#020617")

        # =====================
        # CENTER CONTAINER
        # =====================
        self.container = tk.Frame(self, bg="#020617")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # =====================
        # TITLE
        # =====================
        self.title = tk.Label(
            self.container,
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#020617"
        )
        self.title.pack(pady=(0, 20))

        # =====================
        # DIFFICULTY
        # =====================
        diff_card = tk.Frame(self.container, bg="#0f172a", padx=20, pady=15)
        diff_card.pack(pady=10)

        self.diff_var = tk.StringVar(value="normal")

        self.diff_label = tk.Label(
            diff_card,
            fg="white",
            bg="#0f172a",
            font=("Segoe UI", 12, "bold")
        )
        self.diff_label.pack(anchor="w", pady=(0, 10))

        def radio(text, value):
            return tk.Radiobutton(
                diff_card,
                text=text,
                variable=self.diff_var,
                value=value,
                indicatoron=0,
                width=20,
                pady=6,
                font=("Segoe UI", 11),
                bg="#1e293b",
                fg="white",
                selectcolor="#334155",
                activebackground="#334155",
                relief="flat"
            )

        self.rb_easy = radio("", "easy")
        self.rb_normal = radio("", "normal")
        self.rb_hard = radio("", "hard")

        self.rb_easy.pack(pady=3)
        self.rb_normal.pack(pady=3)
        self.rb_hard.pack(pady=3)

        # =====================
        # BUTTONS
        # =====================
        def btn(text, cmd, color):
            return tk.Button(
                self.container,
                text=text,
                command=cmd,
                font=("Segoe UI", 13, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2"
            )

        self.btn_new = btn("", lambda: self.switch("game", True, self.diff_var.get()), "#2563eb")
        self.btn_new.pack(pady=8, fill="x")

        self.btn_continue = btn("", lambda: self.switch("game", False, self.diff_var.get()), "#475569")
        self.btn_continue.pack(pady=5, fill="x")

        # =====================
        # LANGUAGE
        # =====================
        lang_frame = tk.Frame(self.container, bg="#020617")
        lang_frame.pack(pady=15)

        tk.Button(lang_frame, text="EN", command=lambda: self.set_lang("en"),
                  bg="#1e293b", fg="white", width=5).pack(side="left", padx=5)

        tk.Button(lang_frame, text="UA", command=lambda: self.set_lang("uk"),
                  bg="#1e293b", fg="white", width=5).pack(side="left", padx=5)

        self.refresh()

    # =====================
    # LANGUAGE CHANGE
    # =====================
    def set_lang(self, lang):
        LANG.set(lang)
        self.refresh()

        # 🔥 важливо: оновити гру якщо вона існує
        if hasattr(self.master, "game") and self.master.game:
            if hasattr(self.master.game, "refresh"):
                self.master.game.refresh()

    # =====================
    # FULL UI REFRESH (FIX)
    # =====================
    def refresh(self):
        t = LANG.t

        self.title.config(text=t("title"))

        self.btn_new.config(text=t("new_game"))
        self.btn_continue.config(text=t("continue"))

        self.diff_label.config(text=t("difficulty"))

        self.rb_easy.config(text="🟢 " + t("easy"))
        self.rb_normal.config(text="🟡 " + t("normal"))
        self.rb_hard.config(text="🔴 " + t("hard"))