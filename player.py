from dataclasses import dataclass, field
import pygame
from pygame import Rect
from pygame.math import Vector2

DIRECTIONS = (Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0))
ALL_POWERS = ("speedup", "slowdown", "invert")


def powers_default():
    return {p: 0 for p in ALL_POWERS}


@dataclass
class Player:
    pos: Vector2
    orig_pos: Vector2
    bounds_tl: Vector2
    keys: tuple[int, int, int, int]
    speed: int = 100
    on_ice: bool = False
    slip: Vector2 = field(default_factory=Vector2)
    current_level: int = 0
    level_data: list = field(default_factory=list)
    powers: dict = field(default_factory=powers_default)

    def handle_collisions(self, collisions, chosen_levels, last_move, screen):
        self.on_ice = False
        
        for collision in collisions:
            if collision == "boundary":
                self.pos -= last_move
                continue
            elif collision == "end":
                self.current_level += 1
                if self.current_level >= len(chosen_levels):
                    font = pygame.font.Font('./Roboto.ttf', 50)
                    text = font.render("You win", False, (255, 255, 255))
                    screen.blit(text, Vector2(0, 0))
                    
                    return False
                self.respawn()
                break
            
            cell = chosen_levels[self.current_level][collision[1]][collision[0]]
            if cell in {"wall", "boundary"} or cell.startswith("door"):
                self.pos -= last_move
            elif cell in {"lava", "spike"}:
                self.respawn()
            elif cell == "ice" and last_move != Vector2(0, 0):
                self.on_ice = True
                self.slip = last_move
            elif cell.startswith("key"):
                self.level_data[self.current_level][cell] = True
            elif cell == "button":
                self.level_data[self.current_level][cell] = True
            elif cell == "power":
                power_type = self.level_data[self.current_level][collision][1]
                self.level_data[self.current_level][collision][0] = True
                self.powers[power_type] = 5

        if not self.on_ice:
            self.slip = Vector2(0, 0)

        return True

    def respawn(self):
        self.pos = self.orig_pos.copy()

        for i in self.level_data[self.current_level]:
            if isinstance(i, str) and i.startswith("key"):
                self.level_data[self.current_level][i] = False

    def decrement_powers(self, dt: float):
        for p in self.powers.keys():
            self.powers[p] = max(self.powers[p] - dt, 0)

        self.slip /= 1.5

    def recalculate_speed(self, other):
        if (
            self.powers["speedup"] > 0
            and self.powers["speedup"] > other.powers["slowdown"]
        ):
            self.speed = 200
        elif (
            other.powers["slowdown"] > 0
            and other.powers["slowdown"] > self.powers["speedup"]
        ):
            self.speed = 50
        else:
            self.speed = 100

        if other.powers["invert"] > 0:
            self.speed *= -1
        
    def reset_buttons(self):
        for level in self.level_data:
            level["button"] = False

    def get_rect(self):
        return Rect(self.pos.x, self.pos.y, 40, 40)

    def get_offset(self, input_keys: tuple[int, ...]):
        offset = Vector2(0, 0)

        for key, direction in zip(self.keys, DIRECTIONS):
            if input_keys[key]:
                offset += direction

        if offset == Vector2(0, 0):
            return offset

        return offset.normalize() * self.speed
