"""Sprite used for equipment pickups and enemy drops."""
import pygame


class Item(pygame.sprite.Sprite):
    """A simple pick‑up item that equips the player."""

    def __init__(self, pos, item_type, name):
        super().__init__()
        self.item_type = item_type
        self.name = name
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # color code by type
        color = (200, 200, 0) if item_type == "weapon" else (0, 0, 200)
        self.image.fill(color)
        self.rect = self.image.get_rect(midbottom=pos)
