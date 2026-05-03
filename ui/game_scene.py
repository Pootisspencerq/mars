import tkinter as tk
from tkinter import messagebox
import random, json, os
from localization.lang import LANG

MAP_SIZE = 5
TARGET_TURNS = 30
SAVE_FILE = "save.json"

BUILD = {
    "S": ("☀️", 15, "energy"),
    "W": ("💧", 20, "water"),
    "O": ("🌿", 20, "oxygen"),
    "M": ("⛏️", 25, "materials")
}

# =====================
# STATE
# =====================

class Cell:
    def __init__(self, t=".", l=0):
        self.t = t
        self.l = l

    def to_dict(self):
        return {"t": self.t, "l": self.l}

    @staticmethod
    def from_dict(d):
        return Cell(d["t"], d["l"])


class GameState:

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.res = {"energy":120,"water":120,"oxygen":120,"materials":120}
        self.population = 10
        self.turn = 0
        self.map = [[Cell() for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        self.map[2][2] = Cell("H",1)

    def to_dict(self):
        return {
            "res": self.res,
            "population": self.population,
            "turn": self.turn,
            "map": [[c.to_dict() for c in row] for row in self.map]
        }

    def load_dict(self, d):
        self.res = d["res"]
        self.population = d["population"]
        self.turn = d["turn"]
        self.map = [[Cell.from_dict(c) for c in row] for row in d["map"]]


# =====================
# ENGINE
# =====================

class GameEngine:
    def __init__(self, state, scene):
        self.state = state
        self.scene = scene

    def build(self, x, y, b):
        c = self.state.map[x][y]
        if c.t != ".":
            return LANG.t("err_occupied")

        _, cost, _ = BUILD[b]
        if self.state.res["materials"] < cost:
            return LANG.t("err_materials")

        self.state.res["materials"] -= cost
        self.state.map[x][y] = Cell(b,1)
        return LANG.t("built")

    def upgrade(self, x, y):
        c = self.state.map[x][y]
        if c.t in [".","H"]:
            return LANG.t("err_upgrade")

        cost = 10 * c.l
        if self.state.res["materials"] < cost:
            return LANG.t("err_materials")

        self.state.res["materials"] -= cost
        c.l += 1
        return LANG.t("upgraded")

    def next_turn(self):
        for row in self.state.map:
            for c in row:
                if c.t in BUILD:
                    _,_,prod = BUILD[c.t]
                    self.state.res[prod] += 10 * c.l

        pop = self.state.population
        mult = self.scene.mult

        self.state.res["energy"] -= int(2 * pop * mult)
        self.state.res["water"] -= int(pop * mult)
        self.state.res["oxygen"] -= int(pop * mult)

        if self.state.res["oxygen"] > 50:
            self.state.population += 1

        event = ""
        if random.random() < self.scene.event_chance:
            e = random.choice(["storm","meteor","bonus"])

            if e == "storm":
                self.state.res["energy"] -= 15
                event = LANG.t("event_storm")

            elif e == "meteor":
                self.state.res["materials"] -= 20
                event = LANG.t("event_meteor")

            elif e == "bonus":
                self.state.res["water"] += 20
                event = LANG.t("event_bonus")

        self.state.turn += 1
        return event


# =====================
# GAME SCENE
# =====================

class GameScene(tk.Frame):
        # ===== DIFFICULTY =====
    def set_difficulty(self, diff):
        self.difficulty = diff

        if diff == "easy":
            self.state.res = {
                "energy":150,
                "water":150,
                "oxygen":150,
                "materials":150
            }
            self.mult = 0.7
            self.event_chance = 0.1

        elif diff == "normal":
            self.state.res = {
                "energy":120,
                "water":120,
                "oxygen":120,
                "materials":120
            }
            self.mult = 1.0
            self.event_chance = 0.25

        elif diff == "hard":
            self.state.res = {
                "energy":80,
                "water":80,
                "oxygen":80,
                "materials":80
            }
            self.mult = 1.5
            self.event_chance = 0.4
    def __init__(self, master, switch):
        super().__init__(master)

        self.switch = switch
        self.state = GameState()

        self.mult = 1.0
        self.event_chance = 0.25

        self.engine = GameEngine(self.state, self)

        self.mode = "build"
        self.selected = None

        self.base_font = 10
        self.ui_scale = 1.0

        self.configure(bg="#1e1e1e")

        # ===== TOP HUD =====
        self.top = tk.Frame(self, bg="#111")
        self.top.pack(fill="x")

        self.hud = tk.Frame(self.top, bg="#111")
        self.hud.pack(pady=5)

        def make_item(icon):
            f = tk.Frame(self.hud, bg="#222", padx=6, pady=3)
            f.pack(side="left", padx=4)
            tk.Label(f, text=icon, bg="#222", fg="white").pack(side="left")
            val = tk.Label(f, text="0", bg="#222", fg="white")
            val.pack(side="left")
            return val

        self.h_energy = make_item("⚡")
        self.h_water = make_item("💧")
        self.h_oxygen = make_item("🌿")
        self.h_mat = make_item("⛏")
        self.h_pop = make_item("👥")
        self.h_turn = make_item("⏱")

        # ===== MAIN =====
        main = tk.Frame(self, bg="#1e1e1e")
        main.pack(expand=True, fill="both")

        self.grid_frame = tk.Frame(main, bg="#1e1e1e")
        self.grid_frame.pack(side="left", expand=True, fill="both")

        self.buttons = []

        for i in range(MAP_SIZE):
            row = []
            for j in range(MAP_SIZE):
                b = tk.Button(self.grid_frame, bg="#2d2d2d", fg="white", relief="flat")
                b.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

                b.config(command=lambda x=i,y=j:self.click(x,y))

                b.bind("<Enter>", lambda e: e.widget.config(bg="#666"))
                b.bind("<Leave>", lambda e: e.widget.config(bg="#2d2d2d"))

                row.append(b)
            self.buttons.append(row)

        for i in range(MAP_SIZE):
            self.grid_frame.rowconfigure(i, weight=1)
            self.grid_frame.columnconfigure(i, weight=1)

        # ===== BOTTOM =====
        self.bottom = tk.Frame(self, bg="#111")
        self.bottom.pack(fill="x")

        self.build_buttons = {}

        for b in BUILD:
            btn = tk.Button(self.bottom, text=BUILD[b][0], bg="#333", fg="white",
                            command=lambda x=b:self.select(x))
            btn.pack(side="left", padx=2)
            self.build_buttons[b] = btn

        self.upgrade_btn = tk.Button(self.bottom, text="⬆️", command=self.set_upgrade)
        self.upgrade_btn.pack(side="left", padx=2)

        self.turn_btn = tk.Button(self.bottom, text="⏭", command=self.next_turn)
        self.turn_btn.pack(side="right", padx=5)

        # STATUS
        self.status = tk.Label(self, fg="white", bg="#000")
        self.status.pack(fill="x")

        self.bind("<Configure>", self.on_resize)

        self.pulse_turn_button()
        self.update_ui()

    # ===== ANIMATIONS =====
    def animate_click(self, btn):
        orig = btn["bg"]
        btn.config(bg="#999")
        self.after(100, lambda: btn.config(bg=orig))

    def animate_build(self, btn, color):
        btn.config(bg="#000")
        self.after(120, lambda: btn.config(bg=color))

    def animate_status(self, color):
        self.status.config(bg=color)
        self.after(200, lambda: self.status.config(bg="#000"))

    def pulse_turn_button(self):
        def pulse():
            self.turn_btn.config(bg="#666")
            self.after(300, lambda: self.turn_btn.config(bg="#333"))
            self.after(700, pulse)
        pulse()

    # ===== SCALING =====
    def on_resize(self, event):
        scale = min(event.width / 1000, event.height / 700)
        scale = max(0.6, min(scale, 1.8))

        if abs(scale - self.ui_scale) < 0.05:
            return

        self.ui_scale = scale
        self.apply_scale()

    def apply_scale(self):
        size = int(self.base_font * self.ui_scale)

        for row in self.buttons:
            for b in row:
                b.config(font=("Arial", size))

        for b in self.build_buttons.values():
            b.config(font=("Arial", size))

        self.upgrade_btn.config(font=("Arial", size))
        self.turn_btn.config(font=("Arial", size))
        self.status.config(font=("Arial", size))

    # ===== GAME =====
    def select(self, b):
        self.mode = "build"
        self.selected = b

    def set_upgrade(self):
        self.mode = "upgrade"

    def click(self, x, y):
        btn = self.buttons[x][y]
        self.animate_click(btn)

        if self.mode == "build" and self.selected:
            msg = self.engine.build(x,y,self.selected)
        else:
            msg = self.engine.upgrade(x,y)

        c = self.state.map[x][y]

        if c.t in BUILD:
            self.animate_build(btn, "#3a3a3a")

        self.status.config(text=msg)
        self.update_ui()

    def next_turn(self):
        event = self.engine.next_turn()

        if "storm" in event.lower():
            self.animate_status("#550000")
        elif "bonus" in event.lower():
            self.animate_status("#003300")

        if self.state.turn >= TARGET_TURNS:
            messagebox.showinfo("Win", LANG.t("win"))
            self.switch("menu")
            return

        if any(v <= 0 for v in self.state.res.values()):
            messagebox.showerror("Lose", LANG.t("lose"))
            self.switch("menu")
            return

        self.status.config(text=event)
        self.update_ui()

    # ===== UI =====
    def update_ui(self):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                c = self.state.map[i][j]

                color = {
                    "S":"#FFD54F",
                    "W":"#4FC3F7",
                    "O":"#81C784",
                    "M":"#B0BEC5",
                    "H":"#555"
                }.get(c.t, "#2d2d2d")

                icon = BUILD[c.t][0] if c.t in BUILD else ("🏠" if c.t=="H" else "")
                self.buttons[i][j].config(text=icon, bg=color)

        r = self.state.res
        self.h_energy.config(text=r["energy"])
        self.h_water.config(text=r["water"])
        self.h_oxygen.config(text=r["oxygen"])
        self.h_mat.config(text=r["materials"])
        self.h_pop.config(text=self.state.population)
        self.h_turn.config(text=f"{self.state.turn}/{TARGET_TURNS}")