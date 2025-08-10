import pymunk
from settings import WIDTH, FPS, GRAVITY, GROUND_LEVEL

space: pymunk.Space | None = None

def init():
    global space
    space = pymunk.Space()
    space.gravity = (0, GRAVITY * FPS)
    ground = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground_shape = pymunk.Segment(ground, (0, GROUND_LEVEL), (WIDTH, GROUND_LEVEL), 0)
    ground_shape.friction = 1.0
    space.add(ground, ground_shape)

def update(dt_ms: int):
    if space is None:
        return
    space.step(dt_ms / 1000.0)
