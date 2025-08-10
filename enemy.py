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
=======
import random
import pygame
import pymunk
import physics
from settings import ENEMY_SPEED, FPS
from item import Item


class Enemy(pygame.sprite.Sprite):
    """Simple walking enemy with physics body."""

    def __init__(self, x_pos: float, y_pos: float):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

        # --- Pymunk body & shape ---
        mass = 1
        moment = pymunk.moment_for_box(mass, self.rect.size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly.create_box(self.body, self.rect.size)
        self.shape.elasticity = 0.0

        physics.space.add(self.body, self.shape)

        # Speed is in pixels/frame; convert to pixels/second via FPS in update()
        self.speed = ENEMY_SPEED

    def update(self):
        # Move left at constant horizontal speed; keep current vertical velocity
        self.body.velocity = (-self.speed * FPS, self.body.velocity.y)

        # Sync sprite after the physics step (or at least each update)
        self.sync_with_body()

        # Kill when off-screen
        if self.rect.right < 0:
            self.kill()

    def sync_with_body(self) -> None:
        # Keep the pygame rect aligned with the physics body
        self.rect.center = self.body.position

    def kill(self) -> None:
        # Clean up physics objects before removing the sprite
        if self.body in physics.space.bodies or self.shape in physics.space.shapes:
            try:
                physics.space.remove(self.body, self.shape)
            except Exception:
                # In case they were already removed
                pass
        super().kill()

    # hooks for item drops
    def drop(self):
        """Return an ``Item`` dropped by this enemy or ``None``.

        The default implementation gives a small random chance to drop a
        weapon upgrade. Sub-classes can override this to provide custom drop
        behaviour.
        """
        if random.random() < 0.1:
            return Item(self.rect.midbottom, "weapon", "blaster")
        return None
    main
