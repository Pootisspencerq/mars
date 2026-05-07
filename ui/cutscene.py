import tkinter as tk
from PIL import Image, ImageTk
import os

class Cutscene(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master)

        self.switch = switch
        self.configure(bg="black")

        # ===== IMAGE =====
        self.label = tk.Label(self, bg="black")
        self.label.pack(fill="both", expand=True)

        # ===== TEXT =====
        self.text = tk.Label(
            self,
            text="",
            fg="white",
            bg="#000000",
            font=("Segoe UI", 16),
            wraplength=1000,
            justify="center"
        )
        self.text.place(relx=0.5, rely=0.85, anchor="center")

        # ===== SKIP BUTTON =====
        self.skip_btn = tk.Button(
            self,
            text="Skip ▶",
            command=self.skip,
            bg="#111",
            fg="white"
        )
        self.skip_btn.place(relx=0.95, rely=0.95, anchor="se")

        # ===== LOAD FRAMES =====
        self.frames = []
        self.index = 0

        folder = "assets/cutscene"

        if os.path.exists(folder):
            for f in sorted(os.listdir(folder)):
                if f.endswith(".png") or f.endswith(".jpg"):
                    try:
                        img = Image.open(os.path.join(folder, f))
                        img = img.resize((1280, 800))
                        self.frames.append(ImageTk.PhotoImage(img))
                    except:
                        pass

        # ===== STORY =====
        self.story = [
            "Year 2095...",
            "Humanity is running out of resources...",
            "You are sent to Mars...",
            "Build a colony...",
            "Survive..."
        ]

        # ===== якщо нема кадрів =====
        if not self.frames:
            self.text.config(text="No cutscene files found")
            self.after(2000, self.skip)
            return

        # старт
        self.play()

    def play(self):
        max_len = max(len(self.frames), len(self.story))

        # кінець
        if self.index >= max_len:
            self.after(500, self.skip)
            return

        # IMAGE
        if self.index < len(self.frames):
            frame = self.frames[self.index]
            if frame:
                self.label.config(image=frame)

        # TEXT
        if self.index < len(self.story):
            self.text.config(text=self.story[self.index])

        self.index += 1
        self.after(2000, self.play)

    def skip(self):
        self.switch("menu")