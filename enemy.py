import pygame
import pymunk
import physics
from settings import ENEMY_SPEED, FPS


class Enemy(pygame.sprite.Sprite):
    """Simple walking enemy with physics body."""

    def __init__(self, x_pos: float, y_pos: float):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
        mass = 1
        moment = pymunk.moment_for_box(mass, self.rect.size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly.create_box(self.body, self.rect.size)
        self.shape.elasticity = 0.0
        physics.space.add(self.body, self.shape)
        self.speed = ENEMY_SPEED

    def update(self):
        self.body.velocity = (-self.speed * FPS, self.body.velocity.y)
        if self.rect.right < 0:
            self.kill()

    def sync_with_body(self) -> None:
        self.rect.center = self.body.position

    def kill(self) -> None:
        physics.space.remove(self.body, self.shape)
        super().kill()
