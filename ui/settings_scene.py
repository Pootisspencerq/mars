import tkinter as tk
from tkinter import filedialog, messagebox

from settings import (
    load_settings,
    save_settings,
    reset_settings
)

from localization.lang import (
    set_lang,
    t
)

from audio import set_volume, toggle_mute, restart_music


class SettingsScene(tk.Frame):

    def __init__(self, master, switch):

        super().__init__(master, bg="#020617")

        self.master = master
        self.switch = switch

        self.settings = load_settings()

        # =====================
        # TITLE
        # =====================

        self.title = tk.Label(
            self,
            text=t("settings"),
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#020617"
        )
        self.title.pack(pady=20)

        # =====================
        # CONTAINER
        # =====================

        self.container = tk.Frame(
            self,
            bg="#0f172a",
            padx=25,
            pady=25
        )
        self.container.pack(padx=20, pady=10)

        # =====================
        # LANGUAGE
        # =====================

        self.lang_label = tk.Label(
            self.container,
            text=t("language"),
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#0f172a"
        )
        self.lang_label.pack(anchor="w", pady=(0, 5))

        lang_frame = tk.Frame(self.container, bg="#0f172a")
        lang_frame.pack(fill="x", pady=(0, 15))

        tk.Button(
            lang_frame,
            text="EN",
            width=8,
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=lambda: self.change_language("en")
        ).pack(side="left", padx=5)

        tk.Button(
            lang_frame,
            text="UA",
            width=8,
            bg="#16a34a",
            fg="white",
            relief="flat",
            command=lambda: self.change_language("ua")
        ).pack(side="left", padx=5)

        # =====================
        # SOUND
        # =====================

        self.sound_label = tk.Label(
            self.container,
            text=t("sound"),
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#0f172a"
        )
        self.sound_label.pack(anchor="w", pady=(0, 5))

        self.volume_slider = tk.Scale(
            self.container,
            from_=0,
            to=1,
            resolution=0.1,
            orient="horizontal",
            length=250,
            bg="#0f172a",
            fg="white",
            highlightthickness=0,
            command=self.change_volume
        )
        self.volume_slider.set(self.settings["volume"])
        self.volume_slider.pack(pady=(0, 15))

        # =====================
        # MUTE
        # =====================

        self.mute_var = tk.BooleanVar(value=self.settings["mute"])

        self.mute_check = tk.Checkbutton(
            self.container,
            text=t("mute"),
            variable=self.mute_var,
            bg="#0f172a",
            fg="white",
            selectcolor="#1e293b",
            command=self.change_mute
        )
        self.mute_check.pack(anchor="w", pady=(0, 15))

        # =====================
        # FULLSCREEN
        # =====================

        self.fullscreen_var = tk.BooleanVar(value=self.settings["fullscreen"])

        self.fullscreen_check = tk.Checkbutton(
            self.container,
            text=t("fullscreen"),
            variable=self.fullscreen_var,
            bg="#0f172a",
            fg="white",
            selectcolor="#1e293b",
            command=self.change_fullscreen
        )
        self.fullscreen_check.pack(anchor="w", pady=(0, 15))

        # =====================
        # ANIMATIONS
        # =====================

        self.anim_var = tk.BooleanVar(value=self.settings["animations"])

        self.anim_check = tk.Checkbutton(
            self.container,
            text=t("animations"),
            variable=self.anim_var,
            bg="#0f172a",
            fg="white",
            selectcolor="#1e293b",
            command=self.change_animations
        )
        self.anim_check.pack(anchor="w", pady=(0, 15))

        # =====================
        # FPS
        # =====================

        self.fps_var = tk.BooleanVar(value=self.settings["show_fps"])

        self.fps_check = tk.Checkbutton(
            self.container,
            text=t("show_fps"),
            variable=self.fps_var,
            bg="#0f172a",
            fg="white",
            selectcolor="#1e293b",
            command=self.change_fps
        )
        self.fps_check.pack(anchor="w", pady=(0, 20))

        # =====================
        # MUSIC
        # =====================

        self.music_btn = tk.Button(
            self.container,
            text=t("custom_music"),
            bg="#7c3aed",
            fg="white",
            relief="flat",
            command=self.select_music
        )
        self.music_btn.pack(fill="x", pady=5)

        # =====================
        # SOUNDS
        # =====================

        self.build_btn = tk.Button(
            self.container,
            text=t("custom_build_sound"),
            bg="#2563eb",
            fg="white",
            command=lambda: self.select_sound("custom_build_sound")
        )
        self.build_btn.pack(fill="x", pady=5)

        self.click_btn = tk.Button(
            self.container,
            text=t("custom_click_sound"),
            bg="#0ea5e9",
            fg="white",
            command=lambda: self.select_sound("custom_click_sound")
        )
        self.click_btn.pack(fill="x", pady=5)

        self.event_btn = tk.Button(
            self.container,
            text=t("custom_event_sound"),
            bg="#f59e0b",
            fg="white",
            command=lambda: self.select_sound("custom_event_sound")
        )
        self.event_btn.pack(fill="x", pady=5)

        # =====================
        # RESET
        # =====================

        self.reset_btn = tk.Button(
            self.container,
            text=t("reset_settings"),
            bg="#dc2626",
            fg="white",
            command=self.reset_all
        )
        self.reset_btn.pack(fill="x", pady=(20, 5))

        # =====================
        # BACK
        # =====================

        self.back_btn = tk.Button(
            self,
            text=f"⬅ {t('menu')}",
            bg="#374151",
            fg="white",
            command=lambda: self.switch("menu")
        )
        self.back_btn.pack(pady=20)

    # =====================
    # TRANSLATION FIX
    # =====================

    def refresh_ui(self):

        self.title.config(text=t("settings"))
        self.lang_label.config(text=t("language"))
        self.sound_label.config(text=t("sound"))

        self.mute_check.config(text=t("mute"))
        self.fullscreen_check.config(text=t("fullscreen"))
        self.anim_check.config(text=t("animations"))
        self.fps_check.config(text=t("show_fps"))

        self.music_btn.config(text=t("custom_music"))
        self.build_btn.config(text=t("custom_build_sound"))
        self.click_btn.config(text=t("custom_click_sound"))
        self.event_btn.config(text=t("custom_event_sound"))

        self.reset_btn.config(text=t("reset_settings"))
        self.back_btn.config(text=f"⬅ {t('menu')}")

    # =====================
    # LOGIC
    # =====================

    def change_language(self, lang):
        self.settings["language"] = lang
        save_settings(self.settings)
        set_lang(lang)
        self.refresh_ui()
        messagebox.showinfo("INFO", t("saved"))

    def change_volume(self, value):
        self.settings["volume"] = float(value)
        save_settings(self.settings)
        set_volume(value)

    def change_mute(self):
        self.settings["mute"] = self.mute_var.get()
        save_settings(self.settings)
        toggle_mute()

    def change_fullscreen(self):
        value = self.fullscreen_var.get()
        self.settings["fullscreen"] = value
        save_settings(self.settings)
        self.master.attributes("-fullscreen", value)

    def change_animations(self):
        self.settings["animations"] = self.anim_var.get()
        save_settings(self.settings)

    def change_fps(self):
        self.settings["show_fps"] = self.fps_var.get()
        save_settings(self.settings)

    # =====================
    # MUSIC
    # =====================

    def select_music(self):

        path = filedialog.askopenfilename(
            title="Select Music",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )

        if path:
            self.settings["custom_music"] = path
            save_settings(self.settings)
            restart_music()
            messagebox.showinfo("OK", "Music applied")

    def select_sound(self, key):

        path = filedialog.askopenfilename(
            title="Select Sound",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )

        if path:
            self.settings[key] = path
            save_settings(self.settings)
            messagebox.showinfo("OK", "Sound updated")

    # =====================
    # RESET
    # =====================

    def reset_all(self):

        reset_settings()
        self.settings = load_settings()
        restart_music()
        self.refresh_ui()

        messagebox.showinfo("RESET", "Settings reset")