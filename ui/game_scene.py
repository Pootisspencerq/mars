# =====================
# SPACE COLONY AI
# FULL GAME + TRANSLATIONS + SOUND + SAVE + FIXED UI
# =====================

import tkinter as tk
from tkinter import messagebox
import os
import random
import pygame
from save_system import save_game, load_game

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
            s = pygame.mixer.Sound(path)
            s.set_volume(SOUND_VOLUME)
            s.play()
    except:
        pass


# =====================
# TRANSLATIONS
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
        "lang": "LANG",
        "win": "YOU WIN",
        "lose": "YOU LOSE",
        "sound": "SOUND",
        "save": "SAVE",
        "load": "CONTINUE"
    },
    "ua": {
        "title": "КОСМІЧНА КОЛОНІЯ AI",
        "actions": "ДІЇ",
        "upgrade": "ПОКРАЩЕННЯ",
        "next": "ХІД",
        "mute": "ЗВУК ВИКЛ",
        "event": "Подія",
        "lang": "МОВА",
        "win": "ТИ ПЕРЕМІГ",
        "lose": "ТИ ПРОГРАВ",
        "sound": "ЗВУК",
        "save": "ЗБЕРЕГТИ",
        "load": "ПРОДОВЖИТИ"
    },
    "es": {
        "title": "COLONIA ESPACIAL AI",
        "actions": "ACCIONES",
        "upgrade": "MEJORAR",
        "next": "SIGUIENTE TURNO",
        "mute": "MUTE",
        "event": "Evento",
        "lang": "IDIOMA",
        "win": "GANASTE",
        "lose": "PERDISTE",
        "sound": "SONIDO",
        "save": "GUARDAR",
        "load": "CONTINUAR"
    }
}


def t(key):
    return TEXT[LANG].get(key, key)


def switch_lang():
    global LANG
    LANG = "ua" if LANG == "en" else "es" if LANG == "ua" else "en"


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
    ("tornado", "Tornado hits", {"materials": -10}),
    ("storm", "Storm", {"energy": -20}),
    ("meteor", "Meteor", {"materials": -30, "energy": -10}),
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
        self.reset()
        self.diff_mult = 1.0

    def set_difficulty(self, difficulty):
        self.diff_mult = {"easy": 0.7, "hard": 1.5}.get(difficulty, 1.0)

    def reset(self):
        self.res = {
            "energy": 120,
            "water": 120,
            "oxygen": 120,
            "materials": 120
        }
        self.population = 10
        self.turn = 0
        self.last_event = "calm"
        self.game_over = False
        self.map = [[Cell() for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        self.map[2][2] = Cell("H", 1)


# =====================
# ENGINE
# =====================

class GameEngine:
    def __init__(self, state):
        self.state = state

    def set_difficulty(self, difficulty):
        self.state.set_difficulty(difficulty)

    def apply_event(self):
        name, desc, effects = random.choice(EVENTS)
        self.state.last_event = desc
        play_sound("event")

        for k, v in effects.items():
            self.state.res[k] = self.state.res.get(k, 0) + v

    def build(self, x, y, b):
        c = self.state.map[x][y]
        if c.t != ".":
            return

        _, cost, prod, _ = BUILD[b]
        if self.state.res["materials"] < cost:
            return

        self.state.res["materials"] -= cost
        self.state.map[x][y] = Cell(b, 1)
        play_sound("build")

    def upgrade(self, x, y):
        c = self.state.map[x][y]
        if c.t in [".", "H"]:
            return

        cost = 10 * c.l
        if self.state.res["materials"] < cost:
            return

        self.state.res["materials"] -= cost
        c.l += 1
        play_sound("upgrade")

    def next_turn(self):
        s = self.state

        for row in s.map:
            for c in row:
                if c.t in BUILD:
                    _, _, prod, _ = BUILD[c.t]
                    s.res[prod] += 5 + c.l * 3

        pop = s.population
        mult = s.diff_mult

        s.res["energy"] -= int(2 * pop * mult)
        s.res["water"] -= int(pop * mult)
        s.res["oxygen"] -= int(pop * mult)

        if s.res["oxygen"] > 50:
            s.population += 1

        if random.random() < 0.3:
            self.apply_event()

        s.turn += 1


# =====================
# UI
# =====================

class GameScene(tk.Frame):
    def set_difficulty(self, difficulty):
        self.state.set_difficulty(difficulty)
        self.engine.set_difficulty(difficulty)
        self.update_ui()
    def __init__(self, master):
        super().__init__(master, bg="#0b1220")

        self.state = GameState()
        self.engine = GameEngine(self.state)

        self.mode = "build"
        self.selected = None

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # LEFT
        self.left = tk.Frame(self, bg="#0b1220")
        self.left.grid(row=0, column=0, sticky="nsew")

        # TOP BAR
        self.topbar = tk.Frame(self.left, bg="#111827", height=50)
        self.topbar.pack(fill="x")

        self.title = tk.Label(self.topbar, text=t("title"),
                              fg="white", bg="#111827",
                              font=("Segoe UI", 16, "bold"))
        self.title.pack(side="left", padx=10)

        tk.Button(self.topbar, text="🌐",
                  command=lambda: (switch_lang(), self.refresh())).pack(side="right")

        # HUD
        self.hud = tk.Label(self.left, bg="#0f172a", fg="white")
        self.hud.pack(fill="x")

        self.event_label = tk.Label(self.left, bg="#0b1220", fg="gray")
        self.event_label.pack()

        # GRID
        self.grid_frame = tk.Frame(self.left, bg="#111827")
        self.grid_frame.pack(expand=True, fill="both")

        self.buttons = []
        for i in range(MAP_SIZE):
            self.grid_frame.rowconfigure(i, weight=1)
            self.grid_frame.columnconfigure(i, weight=1)

            row = []
            for j in range(MAP_SIZE):
                b = tk.Button(self.grid_frame, text="",
                              command=lambda x=i, y=j: self.click(x, y))
                b.grid(row=i, column=j, sticky="nsew")
                row.append(b)
            self.buttons.append(row)

        # RIGHT
        self.right = tk.Frame(self, bg="#0f172a")
        self.right.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.right, text=t("actions"), bg="#0f172a", fg="white").pack()

        for k in BUILD:
            tk.Button(self.right, text=k,
                      command=lambda x=k: self.select(x)).pack(fill="x")

        tk.Button(self.right, text=t("upgrade"),
                  command=self.set_upgrade).pack(fill="x")

        tk.Button(self.right, text=t("next"),
                  command=self.next_turn).pack(fill="x")

        # SAVE / LOAD
        tk.Button(self.right, text=t("save"),
                  command=self.save).pack(fill="x")

        tk.Button(self.right, text=t("load"),
                  command=self.load).pack(fill="x")

        master.bind("<Key>", self.key)

        self.update_ui()

    # =====================
    # SAVE / LOAD FIXED
    # =====================

    def save(self):
        save_game(self.state, self.engine, LANG)
    def load(self):
        data = load_game()
        if not data:
            return

        self.state.res = data["res"]
        self.state.population = data["population"]
        self.state.turn = data["turn"]
        self.state.last_event = data["last_event"]
        self.state.game_over = data["game_over"]
        self.state.diff_mult = data["diff_mult"]

        global LANG
        LANG = data.get("lang", "en")

        # restore map
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                t, l = data["map"][i][j]
                self.state.map[i][j].t = t
                self.state.map[i][j].l = l

        self.update_ui()

        self.state.res = data["res"]
        self.state.population = data["population"]
        self.state.turn = data["turn"]

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                t, l = data["map"][i][j]
                self.state.map[i][j].t = t
                self.state.map[i][j].l = l

            self.update_ui()

    # =====================
    # CORE
    # =====================

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
            self.engine.build(x, y, self.selected)
        elif self.mode == "upgrade":
            self.engine.upgrade(x, y)

        self.update_ui()

    def next_turn(self):
        self.engine.next_turn()
        self.update_ui()

    def key(self, e):
        if e.keysym == "Return":
            self.next_turn()

    def refresh(self):
        self.title.config(text=t("title"))

    # =====================
    # UI
    # =====================

    def update_ui(self):
        r = self.state.res

        self.hud.config(text=f"⚡ {r['energy']} 💧 {r['water']} 🌿 {r['oxygen']} ⛏ {r['materials']} 👥 {self.state.population}")
        self.event_label.config(text=f"{t('event')}: {self.state.last_event}")

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                self.buttons[i][j].config(text=self.state.map[i][j].t)