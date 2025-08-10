import pygame
from bullet import Bullet
from settings import (
    WIDTH,
    PLAYER_SPEED,
    PLAYER_JUMP,
    GRAVITY,
    GROUND_LEVEL,
)


class Player(pygame.sprite.Sprite):
    """Main controllable character."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=pos)
        self.vel_y = 0
        self.on_ground = False
        self.direction = 1
        self.last_shot = 0
        self.shoot_delay = 250  # milliseconds

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.direction = 1
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def jump(self):
        if self.on_ground:
            self.vel_y = -PLAYER_JUMP
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
        self.apply_gravity()
        # keep within screen
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        # ground collision
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
