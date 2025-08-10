import random
import pygame
from settings import ENEMY_SPEED, GROUND_LEVEL
from item import Item


class Enemy(pygame.sprite.Sprite):
    """Simple walking enemy."""

    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x_pos, GROUND_LEVEL))
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    # hooks for item drops
    def drop(self):
        """Return an ``Item`` dropped by this enemy or ``None``.

        The default implementation gives a small random chance to drop a
        weapon upgrade. Sub‑classes can override this to provide custom drop
        behaviour.
        """
        if random.random() < 0.1:
            return Item(self.rect.midbottom, "weapon", "blaster")
        return None
