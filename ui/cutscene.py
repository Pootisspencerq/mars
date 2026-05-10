import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os


class Cutscene(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master)

        self.switch = switch
        self.configure(bg="black")

        # ===== IMAGE LABEL =====
        self.label = tk.Label(self, bg="black")
        self.label.pack(fill="both", expand=True)

        # ===== TEXT =====
        self.text = tk.Label(
            self,
            text="",
            fg="white",
            bg="black",
            font=("Segoe UI", 16)
        )
        self.text.place(relx=0.5, rely=0.85, anchor="center")

        # ===== SKIP =====
        tk.Button(self, text="Skip ▶", command=self.skip, bg="#111", fg="white") \
            .place(relx=0.95, rely=0.95, anchor="se")

        # ===== VIDEO =====
        self.video_path = os.path.join("assets", "cutscene.mp4")

        if not os.path.exists(self.video_path):
            self.text.config(text="No cutscene.mp4 found in assets/")
            self.after(2000, self.skip)
            return

        self.cap = cv2.VideoCapture(self.video_path)

        self.story = [
            "Year 2095...",
            "Humanity is running out of resources...",
            "You are sent to Mars...",
            "Build a colony...",
            "Survive..."
        ]

        self.frame_index = 0
        self.story_index = 0

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.delay = int(1000 / self.fps) if self.fps > 0 else 33

        self.play()

    def play(self):
        ret, frame = self.cap.read()

        if not ret:
            self.cap.release()
            self.after(500, self.skip)
            return

        # BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        img = img.resize((1280, 800))
        photo = ImageTk.PhotoImage(img)

        self.label.config(image=photo)
        self.label.image = photo

        # текст міняється по часу
        if self.frame_index % (int(self.fps) * 2) == 0:
            if self.story_index < len(self.story):
                self.text.config(text=self.story[self.story_index])
                self.story_index += 1

        self.frame_index += 1
        self.after(self.delay, self.play)

    def skip(self):
        try:
            self.cap.release()
        except:
            pass
        self.switch("menu")