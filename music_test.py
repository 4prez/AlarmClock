import pygame
import time
import random
import os, sys

pygame.init()

# set SDL to use the dummy NULL video driver,
#   so it doesn't need a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"

screen = pygame.display.set_mode((160,160))

pygame.mixer.music.load("Rain_thunder.mp3")
pygame.mixer.music.play(1)

while True:
    time.sleep(1)