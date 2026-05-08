import tkinter as tk
from ui.menu_scene import MenuScene
from ui.game_scene import GameScene
from ui.cutscene import Cutscene
from state import STATE


class App:
    def __init__(self, root):
        self.root = root

        root.title("Mars Colony")
        root.geometry("1000x700")
        root.minsize(800, 600)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", self.exit_fullscreen)

        self.fullscreen = False

        # ===== SCENES =====
        self.menu = MenuScene(root, self.switch)
        self.game = GameScene(root, self.switch)
        self.cutscene = Cutscene(root, self.switch)

        root.game = self.game
        root.switch = self.switch
        self.current = None

        # старт з катсцени
        self.switch("cutscene")

    # ===== FULLSCREEN =====
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    # ===== SWITCH =====
    def switch(self, scene, fresh=False, difficulty="normal"):

        if self.current:
            self.current.pack_forget()

        if scene == "cutscene":

            self.current = self.cutscene

        elif scene == "menu":

            self.current = self.menu

        elif scene == "game":

            if fresh or not hasattr(self, "game"):

                self.game = GameScene(self.root, self.switch)
                self.root.game = self.game

            self.current = self.game

            if fresh:
                STATE.reset()
                self.game.state.reset()

            self.game.set_difficulty(difficulty)

        self.current.pack(fill="both", expand=True)

        if scene == "game":
            self.game.update_ui()


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()