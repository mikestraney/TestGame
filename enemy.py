import pygame
from settings import ENEMY_SPEED, GROUND_LEVEL


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
