import pygame
import os

try:
    pygame.mixer.init()
except:
    print("Sound disabled")

SOUND_VOLUME = 0.5
SOUND_MUTED = False
CURRENT_MUSIC = None


def set_volume(v):
    global SOUND_VOLUME

    SOUND_VOLUME = float(v)

    try:
        pygame.mixer.music.set_volume(SOUND_VOLUME * 0.4)
    except:
        pass


def toggle_mute():
    global SOUND_MUTED

    SOUND_MUTED = not SOUND_MUTED

    try:
        if SOUND_MUTED:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    except:
        pass


def play_sound(name):

    if SOUND_MUTED:
        return

    try:
        path = f"assets/{name}.wav"

        if os.path.exists(path):

            sound = pygame.mixer.Sound(path)
            sound.set_volume(SOUND_VOLUME)
            sound.play()

    except Exception as e:
        print("Sound error:", e)


def play_music(track):

    global CURRENT_MUSIC

    if SOUND_MUTED:
        return

    music_map = {
        "menu": "assets/menu_music.mp3",
        "game": "assets/game_music.mp3"
    }

    path = music_map.get(track)

    if not path:
        return

    if not os.path.exists(path):
        print("Music file missing:", path)
        return

    try:
        # 🔥 HARD RESET (важливо)
        pygame.mixer.music.stop()

        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(SOUND_VOLUME * 0.4)
        pygame.mixer.music.play(-1)

        CURRENT_MUSIC = path

    except Exception as e:
        print("Music error:", e)


def stop_music():

    global CURRENT_MUSIC

    CURRENT_MUSIC = None

    try:
        pygame.mixer.music.stop()
    except:
        pass