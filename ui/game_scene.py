# =====================
# SPACE COLONY AI
# FULL GAME + MENU + SAVE/LOAD + DIFFICULTY + SOUND
# FIXED VERSION
# =====================

import tkinter as tk
from tkinter import messagebox
import os
import random
import json
import pygame
from ui.menu_scene import MenuScene
# =====================
# SOUND SYSTEM
# =====================

try:
    pygame.mixer.init()
except:
    print("Sound disabled")

SOUND_VOLUME = 0.5
SOUND_MUTED = False


def set_volume(v):
    global SOUND_VOLUME
    SOUND_VOLUME = float(v)


def toggle_mute():
    global SOUND_MUTED
    SOUND_MUTED = not SOUND_MUTED


def play_sound(name):

    if SOUND_MUTED:
        return

    try:

        path = f"assets/{name}.wav"

        if os.path.exists(path):

            sound = pygame.mixer.Sound(path)
            sound.set_volume(SOUND_VOLUME)
            sound.play()

    except:
        pass


# =====================
# SAVE SYSTEM
# =====================

SAVE_FILE = "save.json"


def save_game(state, lang):

    data = {
        "res": state.res,
        "population": state.population,
        "turn": state.turn,
        "last_event": state.last_event,
        "game_over": state.game_over,
        "diff_mult": state.diff_mult,
        "lang": lang,
        "map": [
            [(c.t, c.l) for c in row]
            for row in state.map
        ]
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_game():

    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "r") as f:
        return json.load(f)


# =====================
# LANGUAGE
# =====================

LANG = "en"

TEXT = {

    "en": {
        "title": "SPACE COLONY AI",
        "actions": "ACTIONS",
        "upgrade": "UPGRADE",
        "next": "NEXT TURN",
        "mute": "MUTE",
        "event": "Event",
        "win": "YOU WIN",
        "lose": "YOU LOSE",
        "sound": "SOUND",
        "save": "SAVE",
        "load": "CONTINUE",
        "menu": "BACK TO MENU",
        "difficulty": "DIFFICULTY",
        "easy": "EASY",
        "normal": "NORMAL",
        "hard": "HARD"
    },

    "ua": {
        "title": "КОСМІЧНА КОЛОНІЯ AI",
        "actions": "ДІЇ",
        "upgrade": "ПОКРАЩЕННЯ",
        "next": "ХІД",
        "mute": "ЗВУК",
        "event": "Подія",
        "win": "ТИ ПЕРЕМІГ",
        "lose": "ТИ ПРОГРАВ",
        "sound": "ЗВУК",
        "save": "ЗБЕРЕГТИ",
        "load": "ПРОДОВЖИТИ",
        "menu": "МЕНЮ",
        "difficulty": "СКЛАДНІСТЬ",
        "easy": "ЛЕГКО",
        "normal": "НОРМАЛЬНО",
        "hard": "ВАЖКО"
    }
}


def t(key):
    return TEXT[LANG].get(key, key)


def switch_lang():

    global LANG

    if LANG == "en":
        LANG = "ua"
    else:
        LANG = "en"


# =====================
# SETTINGS
# =====================

MAP_SIZE = 5

BUILD = {
    "S": ("☀️", 15, "energy", "#facc15"),
    "W": ("💧", 20, "water", "#38bdf8"),
    "O": ("🌿", 20, "oxygen", "#4ade80"),
    "M": ("⛏️", 25, "materials", "#94a3b8")
}

EVENTS = [
    ("calm", "Nothing happens", {}),
    ("storm", "Dust storm", {"energy": -20}),
    ("meteor", "Meteor strike", {"materials": -30}),
    ("scientist", "Scientist breakthrough", {"energy": 20}),
]


# =====================
# STATE
# =====================

class Cell:

    def __init__(self, t=".", l=0):

        self.t = t
        self.l = l


class GameState:

    def __init__(self):

        self.diff_mult = 1.0
        self.reset()

    def set_difficulty(self, difficulty):

        self.diff_mult = {
            "easy": 0.7,
            "normal": 1.0,
            "hard": 1.5
        }.get(difficulty, 1.0)

    def reset(self):

        self.res = {
            "energy": 120,
            "water": 120,
            "oxygen": 120,
            "materials": 120
        }

        self.population = 10
        self.turn = 0
        self.last_event = "None"
        self.game_over = False

        self.map = [
            [Cell() for _ in range(MAP_SIZE)]
            for _ in range(MAP_SIZE)
        ]

        self.map[2][2] = Cell("H", 1)


# =====================
# ENGINE
# =====================

class GameEngine:

    def __init__(self, state):

        self.state = state

    def apply_event(self):

        name, desc, effects = random.choice(EVENTS)

        self.state.last_event = desc

        play_sound("event")

        for k, v in effects.items():

            self.state.res[k] += v

    def build(self, x, y, b):

        c = self.state.map[x][y]

        if c.t != ".":
            return False

        _, cost, _, _ = BUILD[b]

        if self.state.res["materials"] < cost:
            return False

        self.state.res["materials"] -= cost

        self.state.map[x][y] = Cell(b, 1)

        play_sound("build")

        return True

    def upgrade(self, x, y):

        c = self.state.map[x][y]

        if c.t in [".", "H"]:
            return False

        cost = 10 * c.l

        if self.state.res["materials"] < cost:
            return False

        self.state.res["materials"] -= cost

        c.l += 1

        play_sound("upgrade")

        return True

    def next_turn(self):

        s = self.state

        # production
        for row in s.map:
            for c in row:

                if c.t in BUILD:

                    _, _, prod, _ = BUILD[c.t]

                    s.res[prod] += 5 + c.l * 3

        # consume
        pop = s.population
        mult = s.diff_mult

        s.res["energy"] -= int(2 * pop * mult)
        s.res["water"] -= int(pop * mult)
        s.res["oxygen"] -= int(pop * mult)

        # growth
        if s.res["oxygen"] > 50:
            s.population += 1

        # random event
        if random.random() < 0.35:
            self.apply_event()

        s.turn += 1




    def make_btn(self, text, color, cmd):

        tk.Button(
            self,
            text=text,
            font=("Segoe UI", 16, "bold"),
            bg=color,
            fg="white",
            relief="flat",
            activebackground=color,
            cursor="hand2",
            command=cmd
        ).pack(
            fill="x",
            padx=250,
            pady=12,
            ipady=12
        )

    def new_game(self):

        self.forget()

        game = GameScene(self.master)

        game.pack(fill="both", expand=True)

    def continue_game(self):

        self.forget()

        game = GameScene(self.master)

        game.pack(fill="both", expand=True)

        game.load()


# =====================
# GAME
# =====================

class GameScene(tk.Frame):

    def __init__(self, master, switch):

        super().__init__(master, bg="#0b1220")

        self.master = master
        self.switch = switch
        self.state = GameState()
        self.engine = GameEngine(self.state)

        self.selected = None
        self.mode = "build"

        # =====================
        # LAYOUT
        # =====================

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        # =====================
        # LEFT
        # =====================

        self.left = tk.Frame(self, bg="#0b1220")

        self.left.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # TOP BAR

        self.topbar = tk.Frame(
            self.left,
            bg="#111827",
            height=60
        )

        self.topbar.pack(fill="x")

        self.title = tk.Label(
            self.topbar,
            text=t("title"),
            bg="#111827",
            fg="white",
            font=("Segoe UI", 18, "bold")
        )

        self.title.pack(
            side="left",
            padx=15,
            pady=10
        )

        tk.Button(
            self.topbar,
            text="🌐",
            font=("Segoe UI", 12),
            command=self.change_language
        ).pack(
            side="right",
            padx=10
        )

        # HUD

        self.hud = tk.Label(
            self.left,
            bg="#0f172a",
            fg="white",
            font=("Consolas", 13),
            pady=8
        )

        self.hud.pack(fill="x")

        self.event_label = tk.Label(
            self.left,
            bg="#0b1220",
            fg="#94a3b8",
            font=("Segoe UI", 11)
        )

        self.event_label.pack(pady=5)

        # =====================
        # GRID
        # =====================

        self.grid_frame = tk.Frame(
            self.left,
            bg="#111827"
        )

        self.grid_frame.pack(
            expand=True,
            fill="both",
            padx=12,
            pady=12
        )

        self.buttons = []

        for i in range(MAP_SIZE):

            self.grid_frame.rowconfigure(i, weight=1)
            self.grid_frame.columnconfigure(i, weight=1)

            row = []

            for j in range(MAP_SIZE):

                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Segoe UI Emoji", 24),
                    bg="#1f2937",
                    fg="white",
                    relief="flat",
                    activebackground="#374151",
                    cursor="hand2",
                    command=lambda x=i, y=j: self.click(x, y)
                )

                btn.grid(
                    row=i,
                    column=j,
                    sticky="nsew",
                    padx=4,
                    pady=4,
                    ipadx=20,
                    ipady=20
                )

                row.append(btn)

            self.buttons.append(row)

        # =====================
        # RIGHT PANEL
        # =====================

        self.right = tk.Frame(
            self,
            bg="#0f172a",
            width=260
        )

        self.right.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.right.grid_propagate(False)

        tk.Label(
            self.right,
            text=t("actions"),
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=12)

        # BUILD BUTTONS

        for k in BUILD:

            icon, cost, prod, color = BUILD[k]

            tk.Button(
                self.right,
                text=f"{icon} {prod.upper()} ({cost})",
                bg=color,
                fg="black",
                relief="flat",
                font=("Segoe UI", 11, "bold"),
                cursor="hand2",
                command=lambda x=k: self.select(x)
            ).pack(
                fill="x",
                padx=12,
                pady=4,
                ipady=8
            )

        # ACTIONS

        tk.Button(
            self.right,
            text=f"⬆ {t('upgrade')}",
            bg="#8b5cf6",
            fg="white",
            relief="flat",
            command=self.set_upgrade
        ).pack(
            fill="x",
            padx=12,
            pady=8,
            ipady=8
        )

        tk.Button(
            self.right,
            text=f"⏭ {t('next')}",
            bg="#10b981",
            fg="black",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            command=self.next_turn
        ).pack(
            fill="x",
            padx=12,
            pady=4,
            ipady=10
        )

        # SAVE

        tk.Button(
            self.right,
            text=f"💾 {t('save')}",
            command=self.save
        ).pack(fill="x", padx=12, pady=4)

        tk.Button(
            self.right,
            text=f"📂 {t('load')}",
            command=self.load
        ).pack(fill="x", padx=12, pady=4)

        # DIFFICULTY

        tk.Label(
            self.right,
            text=t("difficulty"),
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=10)

        tk.Button(
            self.right,
            text=t("easy"),
            command=lambda: self.set_difficulty("easy")
        ).pack(fill="x", padx=12, pady=2)

        tk.Button(
            self.right,
            text=t("normal"),
            command=lambda: self.set_difficulty("normal")
        ).pack(fill="x", padx=12, pady=2)

        tk.Button(
            self.right,
            text=t("hard"),
            command=lambda: self.set_difficulty("hard")
        ).pack(fill="x", padx=12, pady=2)

        # SOUND

        tk.Label(
            self.right,
            text=t("sound"),
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=10)

        self.vol = tk.Scale(
            self.right,
            from_=0,
            to=1,
            resolution=0.1,
            orient="horizontal",
            command=set_volume
        )

        self.vol.set(SOUND_VOLUME)

        self.vol.pack(fill="x", padx=12)

        tk.Button(
            self.right,
            text=t("mute"),
            command=toggle_mute
        ).pack(fill="x", padx=12, pady=5)

        # MENU

        tk.Button(
            self.right,
            text=f"🏠 {t('menu')}",
            bg="#374151",
            fg="white",
            relief="flat",
            command=self.back_to_menu
        ).pack(
            fill="x",
            padx=12,
            pady=20,
            ipady=8
        )

        # KEYBOARD

        self.master.bind("<Return>", lambda e: self.next_turn())
        self.master.bind("s", lambda e: self.select("S"))
        self.master.bind("w", lambda e: self.select("W"))
        self.master.bind("o", lambda e: self.select("O"))
        self.master.bind("m", lambda e: self.select("M"))

        self.update_ui()

    # =====================
    # FUNCTIONS
    # =====================

    
    def back_to_menu(self):

        play_sound("click")

        self.master.unbind("<Return>")
        self.master.unbind("s")
        self.master.unbind("w")
        self.master.unbind("o")
        self.master.unbind("m")

        self.switch("menu")

    def change_language(self):

        switch_lang()

        self.refresh()

    def refresh(self):

        self.title.config(text=t("title"))

    def set_difficulty(self, difficulty):

        self.state.set_difficulty(difficulty)

        self.update_ui()

    def save(self):

        save_game(self.state, LANG)

        play_sound("click")

        messagebox.showinfo(
            "SAVE",
            "Game Saved!"
        )

    def load(self):

        data = load_game()

        if not data:

            messagebox.showwarning(
                "ERROR",
                "No save found"
            )

            return

        self.state.res = data["res"]
        self.state.population = data["population"]
        self.state.turn = data["turn"]
        self.state.last_event = data["last_event"]
        self.state.game_over = data["game_over"]
        self.state.diff_mult = data["diff_mult"]

        global LANG
        LANG = data.get("lang", "en")

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):

                t2, l2 = data["map"][i][j]

                self.state.map[i][j].t = t2
                self.state.map[i][j].l = l2

        self.refresh()
        self.update_ui()

        play_sound("click")

    def select(self, b):

        self.selected = b
        self.mode = "build"

        play_sound("click")

    def set_upgrade(self):

        self.mode = "upgrade"

        play_sound("click")

    def click(self, x, y):

        if self.state.game_over:
            return

        if self.mode == "build" and self.selected:

            ok = self.engine.build(x, y, self.selected)

            if not ok:
                play_sound("error")

        elif self.mode == "upgrade":

            ok = self.engine.upgrade(x, y)

            if not ok:
                play_sound("error")

        self.update_ui()

    def next_turn(self):

        self.engine.next_turn()

        self.check_game()

        self.update_ui()

    def check_game(self):

        r = self.state.res

        if (
            r["energy"] <= 0 or
            r["water"] <= 0 or
            r["oxygen"] <= 0
        ):

            self.state.game_over = True

            play_sound("lose")

            messagebox.showerror(
                "GAME OVER",
                t("lose")
            )

            self.state.reset()

        if self.state.turn >= 30:

            play_sound("win")

            messagebox.showinfo(
                "VICTORY",
                t("win")
            )

            self.state.reset()

    def update_ui(self):

        r = self.state.res

        self.hud.config(
            text=(
                f"⚡ {r['energy']}     "
                f"💧 {r['water']}     "
                f"🌿 {r['oxygen']}     "
                f"⛏ {r['materials']}     "
                f"👥 {self.state.population}     "
                f"🕒 {self.state.turn}"
            )
        )

        self.event_label.config(
            text=f"{t('event')}: {self.state.last_event}"
        )

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):

                cell = self.state.map[i][j]

                icon = ""

                if cell.t in BUILD:
                    icon = BUILD[cell.t][0]

                elif cell.t == "H":
                    icon = "🏠"

                text = icon

                if cell.l > 1:
                    text += f"\n{cell.l}"

                color = {
                    ".": "#1f2937",
                    "S": "#facc15",
                    "W": "#38bdf8",
                    "O": "#4ade80",
                    "M": "#94a3b8",
                    "H": "#64748b"
                }.get(cell.t, "#1f2937")

                self.buttons[i][j].config(
                    text=text,
                    bg=color
                )


