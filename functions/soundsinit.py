import pygame
from glob import glob
from pathlib import Path


def init(directory):

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.mixer.set_num_channels(32)

    lsounds = glob(f"{directory}/*.mp3")

    sounds = {}
    winsounds = []
    for sound in lsounds:
        filepath = Path(sound)
        if filepath.stem.startswith("Marker"):
            winsounds.append(pygame.mixer.Sound(f"{filepath}"))
        else:
            sounds[filepath.stem] = pygame.mixer.Sound(f"{filepath}")
    return sounds, winsounds

