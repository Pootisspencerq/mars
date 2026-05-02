import tkinter as tk
from ui.menu_scene import MenuScene
from ui.game_scene import GameScene
from state import STATE

class App:
    def __init__(self, root):
        self.root = root

        self.menu = MenuScene(root, self.switch)
        self.game = GameScene(root, self.switch)

        self.current = None
        self.switch("menu")

    def switch(self, scene, fresh=False):
        if self.current:
            self.current.pack_forget()

        if scene == "menu":
            self.current = self.menu
        else:
            if fresh:
                STATE.reset()
            self.current = self.game
            self.game.update_ui()

        self.current.pack(fill="both", expand=True)


root = tk.Tk()
app = App(root)
root.mainloop()