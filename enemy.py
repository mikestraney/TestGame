"""Enemy sprite classes with simple time-based movement."""

from __future__ import annotations

import math
from typing import Sequence, TYPE_CHECKING

import pygame

from animation import Animation, load_sprite_sheet
from settings import ENEMY_SPEED, GROUND_LEVEL, WIDTH

if TYPE_CHECKING:
    from item import Item


class Enemy(pygame.sprite.Sprite):
    """Base enemy class handling movement and animation."""

    def __init__(
        self,
        x_pos: int,
        frames: Sequence[pygame.Surface],
        speed: float,
        frame_time: int,
    ) -> None:
        super().__init__()
        self.animation = Animation(frames, frame_time)
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(midbottom=(x_pos, GROUND_LEVEL))
        self.speed = speed

    def update(self, dt: float) -> None:
        """Advance the animation and move left at ``self.speed``."""
        self.rect.x -= int(self.speed * dt)
        self.animation.update(int(dt * 1000))
        self.image = self.animation.get_frame()
        if self.rect.right < 0:
            self.kill()

    def drop(self) -> "Item | None":
        """Return an item dropped by this enemy, if any."""
        return None


class RunnerEnemy(Enemy):
    """Ground enemy that runs towards the player."""

    def __init__(self, x_pos: int) -> None:
        frames = load_sprite_sheet("assets/runner_sheet.txt", 32, 32)
        super().__init__(x_pos, frames, ENEMY_SPEED, 150)


class FlyerEnemy(Enemy):
    """Flying enemy that oscillates vertically."""

    def __init__(self, x_pos: int) -> None:
        frames = load_sprite_sheet("assets/flyer_sheet.txt", 32, 32)
        super().__init__(x_pos, frames, ENEMY_SPEED * 0.8, 150)
        self.rect.midbottom = (x_pos, GROUND_LEVEL - 120)
        self.base_y = self.rect.y
        self.time = 0.0

    def update(self, dt: float) -> None:
        super().update(dt)
        self.time += dt
        self.rect.y = self.base_y + int(math.sin(self.time * 5) * 20)


class BossEnemy(Enemy):
    """Large enemy that stops near the player."""

    def __init__(self, x_pos: int) -> None:
        frames = load_sprite_sheet("assets/boss_sheet.txt", 64, 64)
        super().__init__(x_pos, frames, ENEMY_SPEED * 0.5, 300)

    def update(self, dt: float) -> None:
        if self.rect.x > WIDTH - 200:
            super().update(dt)
        else:
            self.animation.update(int(dt * 1000))
            self.image = self.animation.get_frame()

