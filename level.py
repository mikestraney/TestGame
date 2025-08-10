"""Level loading and rendering using Tiled maps."""

from __future__ import annotations

import pygame
import pytmx
import pymunk

import physics
from settings import WIDTH, HEIGHT


class Level:
    """Load a `.tmx` map and expose drawing helpers.

    The map is rendered to a surface for quick blitting. Object layers with
    type ``platform`` are converted into static physics bodies so that sprites
    can collide with them.
    """

    def __init__(self, filename: str):
        # Load Tiled map
        self.tmx_data = pytmx.util_pygame.load_pygame(filename)

        # Pre-render visible tile layers to a surface
        map_width = self.tmx_data.width * self.tmx_data.tilewidth
        map_height = self.tmx_data.height * self.tmx_data.tileheight
        self.map_surface = pygame.Surface((map_width, map_height)).convert()
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.map_surface.blit(
                            tile,
                            (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight),
                        )

        # Create parallax background layers
        self.parallax_layers = []
        colors = [(20, 20, 40), (40, 40, 80), (60, 60, 120)]
        speeds = [0.2, 0.5, 1.0]
        for color, speed in zip(colors, speeds):
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill(color)
            self.parallax_layers.append({"surface": surf, "speed": speed, "x": 0.0})

        # Load platforms from object layers into the physics space
        self.platform_rects: list[pygame.Rect] = []
        if physics.space is not None:
            for obj in self.tmx_data.objects:
                if getattr(obj, "type", "") == "platform":
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.platform_rects.append(rect)
                    body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    body.position = rect.center
                    shape = pymunk.Poly.create_box(body, rect.size)
                    shape.friction = 1.0
                    physics.space.add(body, shape)

    def update(self, dt: float) -> None:
        """Update parallax layers.

        Parameters
        ----------
        dt: float
            Milliseconds since last frame.
        """

        for layer in self.parallax_layers:
            layer["x"] = (layer["x"] - layer["speed"]) % WIDTH

    def draw(self, screen: pygame.Surface) -> None:
        """Draw background and map layers to the screen."""

        # Parallax background
        for layer in self.parallax_layers:
            x = -layer["x"]
            screen.blit(layer["surface"], (x, 0))
            screen.blit(layer["surface"], (x + WIDTH, 0))

        # Map layers
        screen.blit(self.map_surface, (0, 0))

