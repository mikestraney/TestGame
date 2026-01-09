import pygame
from typing import List, Tuple


def load_sprite_sheet(path: str, frame_width: int, frame_height: int) -> List[pygame.Surface]:
    """Load frames from a text-based sprite sheet.

    Each non-empty, non-comment line in ``path`` must contain ``R,G,B`` values.
    A ``pygame.Surface`` filled with the specified colour is created for each
    line and returned in the order encountered.
    """
    colors: List[Tuple[int, int, int]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                continue
            try:
                color = tuple(int(p) for p in parts)
            except ValueError:
                continue
            colors.append(color)

    frames: List[pygame.Surface] = []
    for color in colors:
        surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        surface.fill(color)
        frames.append(surface)
    return frames


class Animation:
    """Simple time-based animation helper."""

    def __init__(self, frames: List[pygame.Surface], frame_time: int):
        """frames: surfaces to cycle; frame_time: milliseconds per frame"""
        self.frames = frames
        self.frame_time = frame_time
        self.time = 0
        self.index = 0

    def update(self, dt: int) -> None:
        self.time += dt
        if self.time >= self.frame_time:
            self.time %= self.frame_time
            self.index = (self.index + 1) % len(self.frames)

    def get_frame(self) -> pygame.Surface:
        return self.frames[self.index]
