import pygame
import pymunk
import physics
from bullet import Bullet
from inventory import Inventory
from settings import WIDTH, PLAYER_SPEED, PLAYER_JUMP, GROUND_LEVEL


class Player(pygame.sprite.Sprite):
    """Main controllable character."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=pos)

        # Physics body & shape
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

        # inventory and appearance layers
        self.inventory = Inventory()
        self.update_image()

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Process movement keys and update body velocity."""
        vx = 0
        if keys[pygame.K_LEFT]:
            vx -= PLAYER_SPEED
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            vx += PLAYER_SPEED
            self.direction = 1
        self.body.velocity = (vx, self.body.velocity.y)

        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

    def jump(self) -> None:
        """Give the player an upward impulse if on the ground."""
        if self.on_ground:
            self.body.velocity = (self.body.velocity.x, -PLAYER_JUMP)
            self.on_ground = False

    def shoot(self, bullets_group: pygame.sprite.Group) -> None:
        """Fire a bullet if the weapon's delay has passed."""
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            pos = self.rect.midright if self.direction == 1 else self.rect.midleft
            bullet = Bullet(pos, self.direction)
            bullets_group.add(bullet)
            self.last_shot = now

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle input and refresh appearance."""
        self.handle_input(keys)
        if self.inventory.dirty:
            self.update_image()
            self.inventory.dirty = False

    def sync_with_body(self, platforms: list[pygame.Rect] | None = None) -> None:
        """Keep the sprite aligned with the physics body and check ground."""
        self.rect.center = self.body.position

        if self.rect.left < 0:
            self.rect.left = 0
            self.body.position = (self.rect.centerx, self.body.position.y)
            self.body.velocity = (0, self.body.velocity.y)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.body.position = (self.rect.centerx, self.body.position.y)
            self.body.velocity = (0, self.body.velocity.y)

        if platforms:
            self.on_ground = any(
                abs(self.rect.bottom - rect.top) < 1 and abs(self.body.velocity.y) < 1
                for rect in platforms
            )
        else:
            self.on_ground = (
                abs(self.rect.bottom - GROUND_LEVEL) < 1
                and abs(self.body.velocity.y) < 1
            )

    def update_image(self):
        """Redraw the player's base and any equipped items."""
        midbottom = self.rect.midbottom
        self.image = pygame.Surface((40, 50), pygame.SRCALPHA)
        self.image.fill((0, 255, 0))

        if self.inventory.armor_sprite:
            self.image.blit(self.inventory.armor_sprite, (0, 0))

        if self.inventory.weapon_sprite:
            # draw weapon near the hands on the right side
            weapon_pos = (
                self.image.get_width() - self.inventory.weapon_sprite.get_width(),
                10,
            )
            self.image.blit(self.inventory.weapon_sprite, weapon_pos)

        # keep rect anchor stable after redrawing
        self.rect = self.image.get_rect(midbottom=midbottom)
