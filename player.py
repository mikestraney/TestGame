import pygame
import pymunk
import physics
from bullet import Bullet
from settings import (
    WIDTH,
    PLAYER_SPEED,
    PLAYER_JUMP,
    FPS,
    GROUND_LEVEL,
)


class Player(pygame.sprite.Sprite):
    """Main controllable character."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=pos)
        mass = 1
        moment = pymunk.moment_for_box(mass, self.rect.size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly.create_box(self.body, self.rect.size)
        self.shape.elasticity = 0.0
        physics.space.add(self.body, self.shape)
        self.on_ground = False
        self.direction = 1
        self.last_shot = 0
        self.shoot_delay = 250  # milliseconds

    def handle_input(self, keys):
        vx = 0
        if keys[pygame.K_LEFT]:
            vx -= PLAYER_SPEED * FPS
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            vx += PLAYER_SPEED * FPS
            self.direction = 1
        self.body.velocity = (vx, self.body.velocity.y)
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

    def jump(self):
        if self.on_ground:
            self.body.velocity = (self.body.velocity.x, -PLAYER_JUMP * FPS)
            self.on_ground = False

    def shoot(self, bullets_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            if self.direction == 1:
                pos = self.rect.midright
            else:
                pos = self.rect.midleft
            bullet = Bullet(pos, self.direction)
            bullets_group.add(bullet)
            self.last_shot = now

    def update(self, keys):
        self.handle_input(keys)

    def sync_with_body(self):
        self.rect.center = self.body.position
        if self.rect.left < 0:
            self.rect.left = 0
            self.body.position = (self.rect.centerx, self.body.position.y)
            self.body.velocity = (0, self.body.velocity.y)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.body.position = (self.rect.centerx, self.body.position.y)
            self.body.velocity = (0, self.body.velocity.y)
        self.on_ground = (
            abs(self.rect.bottom - GROUND_LEVEL) < 1
            and abs(self.body.velocity.y) < 1
        )
