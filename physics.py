import pymunk
from settings import FPS, GRAVITY

space: pymunk.Space | None = None

def init():
    global space
    space = pymunk.Space()
    space.gravity = (0, GRAVITY * FPS)

def update(dt_ms: int):
    if space is None:
        return
    space.step(dt_ms / 1000.0)
