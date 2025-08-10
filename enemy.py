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
