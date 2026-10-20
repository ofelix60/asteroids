from typing import override

import pygame

from asteroids.constants import (
    BLINK_RATE,
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from asteroids.entities.circleshape import CircleShape
from asteroids.entities.shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        self.rotation = 0.0
        self.cooldown = 0.0

        self.invuln_timer = 0.0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    @override
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_invulnerable and int(self.invuln_timer * BLINK_RATE) % 2 == 0:
            return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    @override
    def update(self, dt: float) -> None:
        self.cooldown -= dt
        self.invuln_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(dt * -1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt * -1)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_SPACE] and self.cooldown < 0:
            self.shoot()
            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        shot = Shot(self.position.x, self.position.y)
        uv = pygame.Vector2(0, 1)

        rotated_vector = uv.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_with_speed_vector

    @property
    def is_invulnerable(self) -> bool:
        return self.invuln_timer > 0
