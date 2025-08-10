import pygame
import random


class Particle(pygame.sprite.Sprite):
    """Simple particle with fading over time."""

    def __init__(self, pos, velocity, lifespan, color, radius):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.Vector2(velocity)
        self.lifespan = lifespan
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        age = pygame.time.get_ticks() - self.spawn_time
        if age >= self.lifespan:
            self.kill()
        else:
            alpha = max(0, 255 - int(255 * (age / self.lifespan)))
            self.image.set_alpha(alpha)


def emit_smoke(pos, group):
    """Create a burst of gray smoke particles."""
    for _ in range(8):
        vel = (random.uniform(-0.5, 0.5), random.uniform(-1.5, -0.5))
        particle = Particle(pos, vel, 800, (180, 180, 180), random.randint(4, 8))
        group.add(particle)


def emit_sparks(pos, group):
    """Create fast-moving spark particles."""
    for _ in range(12):
        vel = (random.uniform(-2, 2), random.uniform(-2, 0))
        particle = Particle(pos, vel, 400, (255, 200, 50), random.randint(2, 4))
        group.add(particle)


def emit_explosion(pos, group):
    """Explosion composed of sparks and smoke."""
    emit_sparks(pos, group)
    emit_smoke(pos, group)
