import pygame


class Item(pygame.sprite.Sprite):
    """Simple collectible item dropped by enemies."""

    def __init__(self, pos, category: str, name: str):
        super().__init__()
        self.category = category
        self.name = name
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(midbottom=pos)
