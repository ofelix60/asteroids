import random

from asteroids.constants import ASTEROID_MIN_RADIUS, ASTEROID_SCORES
from asteroids.entities.circleshape import CircleShape
from asteroids.logger import log_event


class Asteroid(CircleShape):
    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split", radius=self.radius)

        angle = random.uniform(20, 50)
        velocity_1 = self.velocity.rotate(angle)
        velocity_2 = self.velocity.rotate(angle * -1)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid_1.velocity = velocity_1 * 1.2
        asteroid_2.velocity = velocity_2 * 1.2

    @property
    def points(self) -> int:
        return ASTEROID_SCORES[int(self.radius // ASTEROID_MIN_RADIUS)]
