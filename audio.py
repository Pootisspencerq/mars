import pygame
import os
from settings import load_settings

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
    """Supports custom sounds from settings + fallback assets"""

    if SOUND_MUTED:
        return

    try:
        settings = load_settings()

        mapping = {
            "build": settings.get("custom_build_sound"),
            "click": settings.get("custom_click_sound"),
            "event": settings.get("custom_event_sound")
        }

        path = mapping.get(name)

        # fallback default
        if not path or not os.path.exists(path):
            path = f"assets/{name}.wav"

        if os.path.exists(path):

            sound = pygame.mixer.Sound(path)
            sound.set_volume(SOUND_VOLUME)
            sound.play()

    except Exception as e:
        print("Sound error:", e)




def play_music(track="menu"):
    global CURRENT_MUSIC

    if SOUND_MUTED:
        return

    settings = load_settings()

    custom_music = settings.get("custom_music", "")

    if custom_music and os.path.exists(custom_music):
        path = custom_music
    else:
        music_map = {
            "menu": "assets/menu_music.mp3",
            "game": "assets/game_music.mp3"
        }
        path = music_map.get(track)

    if not path or not os.path.exists(path):
        print("Music missing:", path)
        return

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(SOUND_VOLUME * 0.4)
        pygame.mixer.music.play(-1)

        CURRENT_MUSIC = path

    except Exception as e:
        print("Music error:", e)




def restart_music():
    """Instant reload of music after settings change"""

    try:
        pygame.mixer.music.stop()
        play_music("menu")
    except:
        pass




def stop_music():
    global CURRENT_MUSIC

    CURRENT_MUSIC = None

    try:
        pygame.mixer.music.stop()
    except:
        pass