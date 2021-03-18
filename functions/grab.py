import pygame


def grab(screen, x, y, w, h):
    "Grab part of screen blit on => screenshot"
    sub = screen.subsurface(x, y, w, h)
    screenshot = pygame.Surface((w, h))
    screenshot.blit(sub, (0, 0))
    return screenshot
