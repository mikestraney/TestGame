import math
import pygame

from settings import ENEMY_SPEED, GROUND_LEVEL, WIDTH
from animation import Animation, load_sprite_sheet


class Enemy(pygame.sprite.Sprite):
    """Base enemy class handling movement and animation."""

    def __init__(self, x_pos, frames, speed, frame_time):
        super().__init__()
        self.animation = Animation(frames, frame_time)
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(midbottom=(x_pos, GROUND_LEVEL))
        self.speed = speed

    def update(self, dt: int):
        self.rect.x -= self.speed
        self.animation.update(dt)
        self.image = self.animation.get_frame()
        if self.rect.right < 0:
            self.kill()


class RunnerEnemy(Enemy):
    """Ground enemy that runs towards the player."""

    def __init__(self, x_pos):
        frames = load_sprite_sheet("assets/runner_sheet.txt", 32, 32)
        super().__init__(x_pos, frames, ENEMY_SPEED, 150)
        self.rect.midbottom = (x_pos, GROUND_LEVEL)


class FlyerEnemy(Enemy):
    """Flying enemy that oscillates vertically."""

    def __init__(self, x_pos):
        frames = load_sprite_sheet("assets/flyer_sheet.txt", 32, 32)
        super().__init__(x_pos, frames, ENEMY_SPEED * 0.8, 150)
        self.rect.midbottom = (x_pos, GROUND_LEVEL - 120)
        self.base_y = self.rect.y
        self.time = 0

    def update(self, dt: int):
        super().update(dt)
        self.time += dt
        self.rect.y = self.base_y + int(math.sin(self.time / 200) * 20)


class BossEnemy(Enemy):
    """Large enemy that stops near the player."""

    def __init__(self, x_pos):
        frames = load_sprite_sheet("assets/boss_sheet.txt", 64, 64)
        super().__init__(x_pos, frames, ENEMY_SPEED * 0.5, 300)
        self.rect.midbottom = (x_pos, GROUND_LEVEL)

    def update(self, dt: int):
        if self.rect.x > WIDTH - 200:
            super().update(dt)
        else:
            self.animation.update(dt)
            self.image = self.animation.get_frame()
