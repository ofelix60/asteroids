from __future__ import annotations

import pygame

from asteroids.constants import (
    DESPAWN_MARGIN,
    LINE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        if self.is_off_screen():
            self.kill()

    def collides_with(self, other: CircleShape) -> bool:
        distance = self.position.distance_to(other.position)
        r1, r2 = self.radius, other.radius

        return distance <= r1 + r2

    def is_off_screen(self) -> bool:
        past_boundary = (
            self.position.x < 0 - DESPAWN_MARGIN
            or self.position.x > SCREEN_WIDTH + DESPAWN_MARGIN
            or self.position.y < 0 - DESPAWN_MARGIN
            or self.position.y > SCREEN_HEIGHT + DESPAWN_MARGIN
        )
        return past_boundary
