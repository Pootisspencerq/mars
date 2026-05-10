import tkinter as tk

from ui.menu_scene import MenuScene
from ui.game_scene import GameScene
from ui.cutscene import Cutscene
from ui.settings_scene import SettingsScene  

from state import STATE
from audio import play_music, stop_music


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

        self.current = None

         
        self.menu = None
        self.game = None
        self.cutscene = None
        self.settings = None    

        self.switch("cutscene")


    def switch(self, scene, fresh=False, difficulty="normal"):

        
        if self.current:
            self.current.pack_forget()
            self.current = None


        if scene == "cutscene":
            if not self.cutscene:
                self.cutscene = Cutscene(self.root, self.switch)

            self.current = self.cutscene

        elif scene == "menu":
            if not self.menu:
                self.menu = MenuScene(self.root, self.switch)

            self.current = self.menu
            play_music("menu")


        elif scene == "game":

            if fresh or not self.game:
                self.game = GameScene(self.root, self.switch, difficulty)
                STATE.reset()

            self.current = self.game
            play_music("game")
            self.game.set_difficulty(difficulty)


        elif scene == "settings":
            if not self.settings:
                self.settings = SettingsScene(self.root, self.switch)

            self.current = self.settings

        if not self.current:
            print(f"[ERROR] Scene '{scene}' not found")
            return

        self.current.pack(fill="both", expand=True)

        if scene == "game":
            self.game.update_ui()


    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)



if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()