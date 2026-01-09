"""Track and load equipped items for the player."""
import os
import pygame


class Inventory:
    """Simple inventory holding equipped weapon and armor."""

    def __init__(self):
        self.weapon = None
        self.armor = None
        self.weapon_sprite = None
        self.armor_sprite = None
        # mark dirty so the player updates the first frame
        self.dirty = True

    def equip(self, item_type, name):
        """Equip an item of *item_type* ("weapon" or "armor")."""
        if item_type == "weapon":
            self.weapon = name
            self.weapon_sprite = self._load_sprite(item_type, name)
        elif item_type == "armor":
            self.armor = name
            self.armor_sprite = self._load_sprite(item_type, name)
        self.dirty = True

    def _load_sprite(self, item_type, name):
        """Return a sprite surface for the given item.

        The function looks for an image in ``assets`` named
        ``<item_type>_<name>.png``. If the file is not found a coloured
        placeholder surface is returned instead so the game keeps running
        even without real art assets.
        """
        filename = f"{item_type}_{name}.png"
        path = os.path.join("assets", filename)
        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha()
        # placeholder surfaces: yellow for weapons, blue for armour
        surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        color = (200, 200, 0) if item_type == "weapon" else (0, 0, 200)
        surf.fill(color)
        return surf
