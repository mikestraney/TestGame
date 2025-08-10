import pygame
from typing import Tuple
from settings import WIDTH, BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    """Projectile fired by the player."""

    def __init__(self, pos: Tuple[int, int], direction: int):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = BULLET_SPEED * direction

    def update(self, dt: float) -> None:
        """Move the bullet and remove it when off-screen."""
        self.rect.x += int(self.speed * dt)
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
