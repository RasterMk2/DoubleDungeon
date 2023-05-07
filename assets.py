import pygame
from pygame.transform import scale


def load(file: str) -> pygame.Surface:
    return pygame.image.load(f"./assets/{file}").convert_alpha()


green_slime = scale(load("green_slime.png"), (40, 40))
blue_slime = scale(load("blue_slime.png"), (40, 40))
brick = scale(load("brick.png"), (90, 90))
wall = scale(load("wall.png"), (90, 90))
spikes_off = scale(load("spikes_off.png"), (90, 90))
spikes_on = scale(load("spikes_on.png"), (90, 90))
button_up = scale(load("button_up.png"), (70, 70))
button_down = scale(load("button_down.png"), (70, 70))
key = scale(load("Key.png"), (30, 30))
ice = scale(load("icecube.png"), (90, 90))
door = scale(load("door.png"), (70, 70))
lava = scale(load("lava.png"), (90, 90))
speedup = scale(load("speedup.png"), (30, 30))
slowdown = scale(load("slowdown.png"), (30, 30))
powerup_test = scale(load("powerup_test.png"), (30, 30))
blindness = scale(load("blindness.png"), (30, 30))

POWERS = {
    "speedup": speedup,
    "slowdown": slowdown,
    "invert": powerup_test,
    "blindness": blindness,
}
