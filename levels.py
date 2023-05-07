import assets

from pygame import Rect
from pygame.math import Vector2

import json
from pathlib import Path

from random import sample

levels_folder = Path("./levels/")


def load_level(path: Path):
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Couldn't load {path}")

def lazy_load_level(path: Path):
    def lazy():
        return load_level(path)
    return lazy

def get_collisions(pos: Vector2, level, level_data, level_rect, other_level_data, p_rect: Rect):
    collisions = []
    
    if not level_rect.contains(p_rect):
        collisions.append("boundary")

    if p_rect.top < 0:
        collisions.append("end")
    
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            if not cell:
                continue

            def get_rect(width):
                return Rect(
                    x * 90 + pos.x + (90 - width) / 2,
                    y * 90 + pos.y + (90 - width) / 2,
                    width,
                    width,
                )

            if cell in {"wall", "lava", "ice"}:
                if p_rect.colliderect(get_rect(90)):
                    collisions.append((x, y))

            elif cell == "spike":
                if p_rect.colliderect(get_rect(90)):
                    if other_level_data["button"]:
                        collisions.append((x, y))

            elif cell.startswith("key"):
                if p_rect.colliderect(get_rect(30)):
                    collisions.append((x, y))

            elif cell.startswith("door"):
                if p_rect.colliderect(get_rect(90)):
                    keyname = "key" + cell[4:]
                    if keyname in level_data:
                        if not level_data[keyname]:
                            collisions.append((x, y))

            elif cell.startswith("button"):
                if p_rect.colliderect(get_rect(70)):
                    collisions.append((x, y))

            elif cell == "power":
                if p_rect.colliderect(get_rect(30)) and not level_data[(x, y)][0]:
                    collisions.append((x, y))

    return collisions


def draw_level(screen, pos: Vector2, level, level_data, other_level_data):
    for y, row in enumerate(level):
        for x, cell in enumerate(row):

            def draw(img, width):
                screen.blit(
                    img,
                    pos + Vector2(x * 90 + (90 - width) / 2, y * 90 + (90 - width) / 2),
                )

            if cell == "wall":
                draw(assets.wall, 90)
            elif cell == "lava":
                draw(assets.lava, 90)
            elif cell == "ice":
                draw(assets.ice, 90)
            elif cell == "spike":
                if other_level_data["button"]:
                    draw(assets.spikes_on, 90)
                else:
                    draw(assets.spikes_off, 90)
            else:
                draw(assets.brick, 90)

            if not cell:
                continue

            if cell.startswith("key"):
                if not level_data[cell]:
                    draw(assets.key, 30)

            elif cell.startswith("door"):
                if not level_data["key" + cell[4:]]:
                    draw(assets.wall, 90)
                    draw(assets.door, 70)
            if cell == "button":
                if level_data[cell]:
                    draw(assets.button_down, 70)
                else:
                    draw(assets.button_up, 70)

            elif cell == "power":
                collected, power_type = level_data[(x, y)]

                if not collected:
                    draw(assets.POWERS[power_type], 30)


def sample_levels(diff, n):
    return sample(list(diff.values()), n)

easy = {i.stem: lazy_load_level(i) for i in levels_folder.glob("e*.json")}
medium = {i.stem: lazy_load_level(i) for i in levels_folder.glob("m*.json")}
hard = {i.stem: lazy_load_level(i) for i in levels_folder.glob("h*.json")}

def sample_all_levels(easy_count: int, medium_count: int, hard_count: int):
    return(
        *sample_levels(easy, easy_count),
        *sample_levels(medium, medium_count),
        *sample_levels(hard, hard_count)
    )
