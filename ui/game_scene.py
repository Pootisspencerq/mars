# =====================
# SPACE COLONY AI
# GAME SCENE (SETTINGS REMOVED)
# =====================

import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import copy

from audio import (
    play_sound,
    play_music,
    stop_music
)
from localization.lang import t, register_listener, unregister_listener, get_lang, set_lang

from constants import (
    MAP_SIZE,
    BUILD,
    EVENTS
)

SAVE_FILE = "save.json"


# =====================
# SAVE / LOAD
# =====================

def save_game(state, lang):

    data = {
        "res": state.res,
        "population": state.population,
        "turn": state.turn,
        "last_event": state.last_event,
        "game_over": state.game_over,
        "diff_mult": state.diff_mult,
        "difficulty_name": state.difficulty_name,
        "lang": lang,
        "map": [
            [(c.t, c.l) for c in row]
            for row in state.map
        ]
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_game():

    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================
# STATE
# =====================

class Cell:

    def __init__(self, t=".", l=0):

        self.t = t
        self.l = l


class GameState:

    def __init__(self, difficulty="normal"):

        self.diff_mult = {
            "easy": 0.7,
            "normal": 1.0,
            "hard": 1.5
        }.get(difficulty, 1.0)

        self.difficulty_name = difficulty

        self.reset()


    def reset(self):

        self.res = {
            "energy": 120,
            "water": 120,
            "oxygen": 120,
            "materials": 120
        }

        self.population = 10
        self.turn = 0
        self.last_event = t("no_event")
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

            if k in self.state.res:
                self.state.res[k] += v

    def build(self, x, y, b):

        c = self.state.map[x][y]

        if c.t != ".":

            play_sound("error")

            messagebox.showwarning(
                "ERROR",
                t("err_occupied")
            )

            return False

        _, cost, _, _ = BUILD[b]

        if self.state.res["materials"] < cost:

            play_sound("error")

            messagebox.showwarning(
                "ERROR",
                t("err_materials")
            )

            return False

        self.state.res["materials"] -= cost

        self.state.map[x][y] = Cell(b, 1)

        play_sound("build")

        return True

    def upgrade(self, x, y):

        c = self.state.map[x][y]

        if c.t in [".", "H"]:

            play_sound("error")

            messagebox.showwarning(
                "ERROR",
                t("err_upgrade")
            )

            return False

        cost = 10 * c.l

        if self.state.res["materials"] < cost:

            play_sound("error")

            messagebox.showwarning(
                "ERROR",
                t("err_materials")
            )

            return False

        self.state.res["materials"] -= cost

        c.l += 1

        play_sound("upgrade")

        return True

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

        if (
            s.res["oxygen"] > 50 and
            s.res["water"] > 50 and
            s.res["energy"] > 50
        ):
            s.population += 1

        if random.random() < 0.35:
            self.apply_event()
        else:
            s.last_event = t("no_event")

        s.turn += 1


# =====================
# GAME SCENE
# =====================

class GameScene(tk.Frame):
    def set_difficulty(self, difficulty):
        self.state.difficulty_name = difficulty

        self.state.diff_mult = {
            "easy": 0.7,
            "normal": 1.0,
            "hard": 1.5
        }.get(difficulty, 1.0)
    def refresh_texts(self):
        self.title.config(text=t("title"))
        self.actions_label.config(text=t("actions"))
        self.upgrade_btn.config(text=f"⬆ {t('upgrade')}")
        self.next_btn.config(text=f"⏭ {t('turn')}")
        self.menu_btn.config(text=f"🏠 {t('menu')}")
        self.save_btn.config(text=f"💾 {t('save')}")
        self.load_btn.config(text=f"📂 {t('load')}")
    def __init__(self, master, switch, difficulty="normal"):
        register_listener(self.refresh_texts)
        super().__init__(master, bg="#0b1220")

        self.master = master
        self.switch = switch

        self.state = GameState(difficulty=difficulty if 'difficulty' in locals() else "normal")
        self.engine = GameEngine(self.state)

        self.selected = None
        self.mode = "build"

        self.previous_state = None

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        # LEFT

        self.left = tk.Frame(self, bg="#0b1220")
        self.left.grid(row=0, column=0, sticky="nsew")

        # TOPBAR

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
            font=("Segoe UI", 20, "bold")
        )

        self.title.pack(side="left", padx=15, pady=10)

        self.diff_display = tk.Label(
            self.topbar,
            text="",
            bg="#111827",
            fg="#38bdf8",
            font=("Segoe UI", 11, "bold")
        )

        self.diff_display.pack(side="left", padx=10)

        # HUD

        self.hud = tk.Label(
            self.left,
            bg="#0f172a",
            fg="white",
            font=("Consolas", 13),
            pady=10
        )

        self.hud.pack(fill="x")

        self.event_label = tk.Label(
            self.left,
            bg="#0b1220",
            fg="#94a3b8",
            font=("Segoe UI", 11)
        )

        self.event_label.pack(pady=5)

        # GRID

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

        # RIGHT

        self.right = tk.Frame(
            self,
            bg="#0f172a",
            width=300
        )

        self.right.grid(row=0, column=1, sticky="nsew")
        self.right.grid_propagate(False)

        self.actions_label = tk.Label(
            self.right,
            text=t("actions"),
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 16, "bold")
        )

        self.actions_label.pack(pady=12)

        # BUILD BUTTONS

        self.build_buttons = {}

        for k in BUILD:

            icon, cost, prod, color = BUILD[k]

            btn = tk.Button(
                self.right,
                text=f"{icon} {prod.upper()} ({cost})",
                bg=color,
                fg="black",
                relief="flat",
                font=("Segoe UI", 11, "bold"),
                cursor="hand2",
                command=lambda x=k: self.select(x)
            )

            btn.pack(
                fill="x",
                padx=12,
                pady=4,
                ipady=8
            )

            self.build_buttons[k] = btn

        # UPGRADE

        self.upgrade_btn = tk.Button(
            self.right,
            text=f"⬆ {t('upgrade')}",
            bg="#8b5cf6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.set_upgrade
        )

        self.upgrade_btn.pack(
            fill="x",
            padx=12,
            pady=8,
            ipady=8
        )

        # NEXT TURN

        self.next_btn = tk.Button(
            self.right,
            text=f"⏭ {t('turn')}",
            bg="#10b981",
            fg="black",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            command=self.next_turn
        )

        self.next_btn.pack(
            fill="x",
            padx=12,
            pady=4,
            ipady=10
        )

        # SAVE / LOAD

        self.save_btn = tk.Button(
            self.right,
            text=f"💾 {t('save')}",
            command=self.save
        )

        self.save_btn.pack(fill="x", padx=12, pady=4)

        self.load_btn = tk.Button(
            self.right,
            text=f"📂 {t('load')}",
            command=self.load
        )

        self.load_btn.pack(fill="x", padx=12, pady=4)

        # MENU

        self.menu_btn = tk.Button(
            self.right,
            text=f"🏠 {t('menu')}",
            bg="#374151",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.back_to_menu
        )

        self.menu_btn.pack(
            fill="x",
            padx=12,
            pady=20,
            ipady=8
        )

        play_music("game")

        self.update_ui()

    # =====================
    # NAVIGATION
    # =====================

    def back_to_menu(self):

        play_sound("click")

        stop_music()

        self.switch("menu")

    # =====================
    # SAVE / LOAD
    # =====================

    def save(self):

        save_game(self.state, get_lang())

        play_sound("click")

        messagebox.showinfo(
            t("save"),
            t("saved")
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
        self.state.difficulty_name = data["difficulty_name"]

        set_lang(data.get("lang", "en"))

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):

                t2, l2 = data["map"][i][j]

                self.state.map[i][j].t = t2
                self.state.map[i][j].l = l2

        self.update_ui()

        play_sound("click")

    # =====================
    # BUILD
    # =====================

    def select(self, b):

        self.selected = b
        self.mode = "build"

        play_sound("click")

    def set_upgrade(self):

        self.mode = "upgrade"

        play_sound("click")

    # =====================
    # GAMEPLAY
    # =====================

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

        self.check_game()

        self.update_ui()

    # =====================
    # GAME OVER
    # =====================

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

    # =====================
    # UI UPDATE
    # =====================

    def update_ui(self):

        r = self.state.res

        diff_text = {
            "easy": f"🟢 {t('easy')}",
            "normal": f"🟡 {t('normal')}",
            "hard": f"🔴 {t('hard')}"
        }.get(self.state.difficulty_name, "Normal")

        self.diff_display.config(
            text=f"{t('difficulty')}: {diff_text}"
        )

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
                    text += f"\nLv.{cell.l}"

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