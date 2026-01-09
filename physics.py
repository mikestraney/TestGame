"""Thin wrapper around a global Pymunk ``Space``."""

import pymunk
from settings import GRAVITY

space: pymunk.Space | None = None

def init() -> None:
    """Create the global physics ``Space`` and configure gravity."""
    global space
    space = pymunk.Space()
    space.gravity = (0, GRAVITY)

def update(dt: float) -> None:
    """Advance the physics simulation by ``dt`` seconds."""
    if space is None:
        return
    space.step(dt)
