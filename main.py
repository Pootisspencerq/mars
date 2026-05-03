import tkinter as tk
from ui.menu_scene import MenuScene
from ui.game_scene import GameScene
from state import STATE


class App:
    def __init__(self, root):
        self.root = root

        # ===== WINDOW SETTINGS =====
        root.title("Mars Colony")

        # 🔥 стартовий розмір + мінімальний
        root.geometry("1000x700")
        root.minsize(800, 600)

        # 🔥 дозволяє нормальний ресайз
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # 🔥 fullscreen toggle (F11)
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", self.exit_fullscreen)

        self.fullscreen = False

        # ===== SCENES =====
        self.menu = MenuScene(root, self.switch)
        self.game = GameScene(root, self.switch)

        # щоб меню могло оновлювати гру
        root.game = self.game

        self.current = None
        self.switch("menu")
    
    # ===== FULLSCREEN =====
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    # ===== SCENE SWITCH =====
    def switch(self, scene, fresh=False, difficulty="normal"):
        if self.current:
            self.current.pack_forget()

        if scene == "menu":
            self.current = self.menu

        else:
            if fresh:
                print("Reset game")

                STATE.reset()
                self.game.state.reset()

                # 🔥 встановлюємо складність
                self.game.set_difficulty(difficulty)

            self.current = self.game

            # 🔥 адаптивність
            self.current.pack(fill="both", expand=True)

            self.game.update_ui()

            return

        self.current.pack(fill="both", expand=True)


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()