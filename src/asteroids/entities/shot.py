from asteroids.constants import SHOT_RADIUS
from asteroids.entities.circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
