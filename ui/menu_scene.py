import tkinter as tk

from localization.lang import (
    t,
    set_lang
)

from audio import (
    play_music,
    play_sound
)


class MenuScene(tk.Frame):

    def __init__(self, master, switch):

        super().__init__(master)

        self.master = master
        self.switch = switch

        self.configure(bg="#020617")

        

        

        play_music("menu")


        

        self.container = tk.Frame(
            self,
            bg="#020617"
        )

        self.container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        
      
        

        self.title = tk.Label(
            self.container,
            text="",
            font=("Segoe UI", 30, "bold"),
            fg="white",
            bg="#020617"
        )

        self.title.pack(
            pady=(0, 25)
        )

        
      
        

        self.diff_card = tk.Frame(
            self.container,
            bg="#0f172a",
            padx=20,
            pady=15
        )

        self.diff_card.pack(
            pady=10,
            fill="x"
        )

        self.diff_var = tk.StringVar(
            value="normal"
        )

        self.diff_label = tk.Label(
            self.diff_card,
            text="",
            fg="white",
            bg="#0f172a",
            font=("Segoe UI", 13, "bold")
        )

        self.diff_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        
      
        

        def radio(value):

            return tk.Radiobutton(
                self.diff_card,
                text="",
                variable=self.diff_var,
                value=value,
                indicatoron=0,
                width=24,
                pady=10,
                font=("Segoe UI", 11, "bold"),
                bg="#1e293b",
                fg="white",
                selectcolor="#334155",
                activebackground="#334155",
                activeforeground="white",
                relief="flat",
                cursor="hand2"
            )

        self.rb_easy = radio("easy")
        self.rb_normal = radio("normal")
        self.rb_hard = radio("hard")

        self.rb_easy.pack(
            pady=3,
            fill="x"
        )

        self.rb_normal.pack(
            pady=3,
            fill="x"
        )

        self.rb_hard.pack(
            pady=3,
            fill="x"
        )

        
     
        

        def btn(command, color):

            return tk.Button(
                self.container,
                text="",
                command=command,
                font=("Segoe UI", 13, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief="flat",
                padx=20,
                pady=12,
                cursor="hand2"
            )

        
        
        

        self.btn_new = btn(
            lambda: self.start_new_game(),
            "#2563eb"
        )

        self.btn_new.pack(
            pady=(15, 8),
            fill="x"
        )


        self.btn_continue = btn(
            lambda: self.continue_game(),
            "#475569"
        )

        self.btn_continue.pack(
            pady=5,
            fill="x"
        )


        self.btn_settings = btn(
            lambda: self.switch("settings"),
            "#7c3aed"
        )

        self.btn_settings.pack(
            pady=5,
            fill="x"
        )



        self.btn_exit = btn(
            self.exit_game,
            "#dc2626"
        )

        self.btn_exit.pack(
            pady=(5, 0),
            fill="x"
        )

        lang_frame = tk.Frame(
            self.container,
            bg="#020617"
        )

        lang_frame.pack(
            pady=18
        )

        self.btn_en = tk.Button(
            lang_frame,
            text="EN",
            command=lambda: self.change_lang("en"),
            bg="#1e293b",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            width=7,
            pady=7,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )

        self.btn_en.pack(
            side="left",
            padx=5
        )

        self.btn_ua = tk.Button(
            lang_frame,
            text="UA",
            command=lambda: self.change_lang("ua"),
            bg="#1e293b",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            width=7,
            pady=7,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )

        self.btn_ua.pack(
            side="left",
            padx=5
        )



        self.refresh()



    def start_new_game(self):

        play_sound("click")

        self.switch(
            "game",
            True,
            self.diff_var.get()
        )

    def continue_game(self):

        play_sound("click")

        self.switch(
            "game",
            False,
            self.diff_var.get()
        )


    def exit_game(self):

        play_sound("click")

        self.master.destroy()



    def change_lang(self, lang):

        set_lang(lang)

        play_sound("click")

        self.refresh()

        if hasattr(self.master, "game"):

            if self.master.game:

                if hasattr(self.master.game, "refresh"):

                    self.master.game.refresh()



    def refresh(self):

        self.title.config(
            text=t("title")
        )

        self.btn_new.config(
            text="🚀 " + t("new_game")
        )

        self.btn_continue.config(
            text="📂 " + t("continue")
        )

        self.btn_settings.config(
            text="⚙ " + t("settings")
        )

        self.btn_exit.config(
            text="❌ " + t("exit")
        )

        self.diff_label.config(
            text=t("difficulty")
        )

        self.rb_easy.config(
            text="🟢 " + t("easy")
        )

        self.rb_normal.config(
            text="🟡 " + t("normal")
        )

        self.rb_hard.config(
            text="🔴 " + t("hard")
        )

        self.update_idletasks()