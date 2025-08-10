WIDTH = 800
HEIGHT = 480
FPS = 60

# Movement and physics constants are defined in pixels per second (or
# pixels per second squared for ``GRAVITY``).  They previously used
# per-frame values which caused gameplay to vary with the frame rate.
PLAYER_SPEED = 300       # player horizontal speed (px/s)
PLAYER_JUMP = 900        # initial jump velocity (px/s)
GRAVITY = 48             # downward acceleration (px/s^2)
BULLET_SPEED = 600       # projectile speed (px/s)
ENEMY_SPEED = 180        # base enemy speed (px/s)
SPAWN_DELAY = 2000  # milliseconds
GROUND_LEVEL = HEIGHT - 40
