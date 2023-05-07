import pygame
from pygame.math import Vector2
from random import choice, sample
from pygame import Rect

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))

import assets
import levels
import player

ALL_POWERS = ("speedup", "slowdown", "invert")
P1_BOUNDS = Rect(0, 0, 630, 630)
P2_BOUNDS = Rect(650, 0, 630, 630)


EASY_LEVELS = 1
MEDIUM_LEVELS = 3
HARD_LEVELS = 1

def load_levels(p1, p2):
    chosen_levels = tuple(map(
        lambda a: a(),
        levels.sample_all_levels(EASY_LEVELS, MEDIUM_LEVELS, HARD_LEVELS)
    ))
    for lv in chosen_levels:
        p1_lv_data = {"button": False}
        p2_lv_data = {"button": False}
        for y, row in enumerate(lv):
            
            for x, cell in enumerate(row):
                if not cell:
                    continue
                if cell.startswith("key"):
                    p1_lv_data[cell] = False
                    p2_lv_data[cell] = False
                elif cell == "power":
                    p1_lv_data[(x, y)] = [False, choice(ALL_POWERS)]
                    p2_lv_data[(x, y)] = [False, choice(ALL_POWERS)]

        p1.level_data.append(p1_lv_data)
        p2.level_data.append(p2_lv_data)

    return chosen_levels, p1, p2


def start():
    running = True
    clock = pygame.time.Clock()
    dt = 0

    p1 = player.Player(
        Vector2(295, 565),
        Vector2(295, 565),
        Vector2(0, 0),
        (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
    )
    p2 = player.Player(
        Vector2(945, 565),
        Vector2(945, 565),
        Vector2(650, 0),
        (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
    )

    chosen_levels, p1, p2 = load_levels(p1, p2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        screen.fill("white")

        p1.recalculate_speed(p2)
        p2.recalculate_speed(p1)

        p1_offset = p1.get_offset(keys) * dt + p1.slip
        p2_offset = p2.get_offset(keys) * dt + p2.slip

        p1.pos += p1_offset
        p2.pos += p2_offset

        p1_collisions = levels.get_collisions(
            p1.bounds_tl,
            chosen_levels[p1.current_level],
            p1.level_data[p1.current_level],
            P1_BOUNDS,
            p2.level_data[p2.current_level],
            p1.get_rect(),
        )
        p2_collisions = levels.get_collisions(
            p2.bounds_tl,
            chosen_levels[p2.current_level],
            p2.level_data[p2.current_level],
            P2_BOUNDS,
            p1.level_data[p1.current_level],
            p2.get_rect(),
        )

        p1.reset_buttons()
        p2.reset_buttons()

        running = p1.handle_collisions(p1_collisions, chosen_levels, p1_offset, screen)
        if not running:
            break
        running = p2.handle_collisions(p2_collisions, chosen_levels, p2_offset, screen)
        if not running:
            break
            
        p1.decrement_powers(dt)
        p2.decrement_powers(dt)

        levels.draw_level(
            screen,
            p1.bounds_tl,
            chosen_levels[p1.current_level],
            p1.level_data[p1.current_level],
            p2.level_data[p2.current_level],
        )
        levels.draw_level(
            screen,
            p2.bounds_tl,
            chosen_levels[p2.current_level],
            p2.level_data[p2.current_level],
            p1.level_data[p1.current_level],
        )

        pygame.draw.line(screen, 0, (640, 0), (640, 720), 21)
        pygame.draw.line(screen, 0, (0, 635), (1280, 635), 11)

        screen.blit(assets.green_slime, p1.pos)
        screen.blit(assets.blue_slime, p2.pos)

        pygame.display.flip()
        dt = clock.tick(15) / 1000


if __name__ == "__main__":
    start()

