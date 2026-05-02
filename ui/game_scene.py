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
    def __init__(self, state):
        self.state = state

    def build(self, x, y, b):
        c = self.state.map[x][y]
        if c.t != ".": return "❌"

        _, cost, _ = BUILD[b]
        if self.state.res["materials"] < cost:
            return "❌ materials"

        self.state.res["materials"] -= cost
        self.state.map[x][y] = Cell(b,1)
        return "✅"

    def upgrade(self, x, y):
        c = self.state.map[x][y]
        if c.t in [".","H"]: return "❌"

        cost = 10 * c.l
        if self.state.res["materials"] < cost:
            return "❌ materials"

        self.state.res["materials"] -= cost
        c.l += 1
        return "⬆️"

    def next_turn(self):
        for row in self.state.map:
            for c in row:
                if c.t in BUILD:
                    _,_,prod = BUILD[c.t]
                    self.state.res[prod] += 10 * c.l

        pop = self.state.population
        self.state.res["energy"] -= 2 * pop
        self.state.res["water"] -= pop
        self.state.res["oxygen"] -= pop

        if self.state.res["oxygen"] > 50:
            self.state.population += 1

        self.state.turn += 1

# =====================
# GAME SCENE
# =====================

class GameScene(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master)

        self.switch = switch
        self.state = GameState()
        self.engine = GameEngine(self.state)

        self.mode = "build"
        self.selected = None

        self.configure(bg="#1e1e1e")

        # GRID
        self.grid_frame = tk.Frame(self, bg="#1e1e1e")
        self.grid_frame.pack(pady=10)

        self.buttons = []

        for i in range(MAP_SIZE):
            row = []
            for j in range(MAP_SIZE):
                b = tk.Button(
                    self.grid_frame,
                    width=5, height=2,
                    bg="#2d2d2d", fg="white",
                    command=lambda x=i,y=j:self.click(x,y)
                )
                b.grid(row=i,column=j,padx=1,pady=1)
                row.append(b)
            self.buttons.append(row)

        # CONTROLS
        ctrl = tk.Frame(self, bg="#1e1e1e")
        ctrl.pack()

        self.turn_btn = tk.Button(ctrl, command=self.next_turn, bg="#444", fg="white")
        self.turn_btn.pack(side="left")

        tk.Button(ctrl,text="💾",command=self.save).pack(side="left")
        tk.Button(ctrl,text="📂",command=self.load).pack(side="left")
        tk.Button(ctrl,text="🏠",command=lambda:self.switch("menu")).pack(side="left")

        # BUILD BUTTONS
        build_frame = tk.Frame(self, bg="#1e1e1e")
        build_frame.pack()

        for b in BUILD:
            tk.Button(build_frame, text=BUILD[b][0],
                      command=lambda x=b:self.select(x)).pack(side="left")

        tk.Button(build_frame,text="⬆️",command=self.set_upgrade).pack(side="left")

        # INFO
        self.info = tk.Label(self, fg="white", bg="#1e1e1e")
        self.info.pack()

        self.update_texts()
        self.update_ui()

    # ===== LANG =====
    def update_texts(self):
        self.turn_btn.config(text=LANG.t("turn"))

    # ===== ACTIONS =====
    def select(self, b):
        self.mode = "build"
        self.selected = b

    def set_upgrade(self):
        self.mode = "upgrade"

    def click(self, x, y):
        if self.mode == "build" and self.selected:
            self.engine.build(x,y,self.selected)
        else:
            self.engine.upgrade(x,y)

        self.update_ui()

    def next_turn(self):
        self.engine.next_turn()

        if self.state.turn >= TARGET_TURNS:
            messagebox.showinfo("Win", LANG.t("win"))
            self.switch("menu")

        if any(v <= 0 for v in self.state.res.values()):
            messagebox.showerror("Lose", LANG.t("lose"))
            self.switch("menu")

        self.update_ui()

    # ===== SAVE =====
    def save(self):
        with open(SAVE_FILE,"w") as f:
            json.dump(self.state.to_dict(), f)

    def load(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE) as f:
                self.state.load_dict(json.load(f))
            self.update_ui()

    # ===== UI =====
    def update_ui(self):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                c = self.state.map[i][j]

                if c.t in BUILD:
                    icon = BUILD[c.t][0]
                    color = "#3a3a3a"
                elif c.t == "H":
                    icon = "🏠"
                    color = "#555"
                else:
                    icon = ""
                    color = "#2d2d2d"

                self.buttons[i][j].config(text=icon, bg=color)

        r = self.state.res
        self.info.config(
            text=f"E:{r['energy']}  W:{r['water']}  O:{r['oxygen']}  M:{r['materials']} | Pop:{self.state.population} | Turn:{self.state.turn}"
        )