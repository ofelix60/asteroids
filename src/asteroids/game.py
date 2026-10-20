import pygame

from asteroids.constants import (
    LIFE_SPACING,
    LIVES_RADIUS,
    PLAYER_INVULN_SECONDS,
    PLAYER_LIVES,
    PLAYER_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from asteroids.entities.asteroid import Asteroid
from asteroids.entities.asteroidfield import AsteroidField
from asteroids.entities.player import Player
from asteroids.entities.shot import Shot
from asteroids.logger import log_event, log_state

# from lives import Lives
from src.asteroids.hud.lives import Lives


class Game:
    def __init__(self) -> None:
        self.x, self.y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.updatable: pygame.sprite.Group = pygame.sprite.Group()
        self.drawable: pygame.sprite.Group = pygame.sprite.Group()
        self.player_group: pygame.sprite.Group = pygame.sprite.Group()
        self.asteroids: pygame.sprite.Group = pygame.sprite.Group()
        self.shots: pygame.sprite.Group = pygame.sprite.Group()

        Player.containers = (
            self.player_group,
            self.updatable,
            self.drawable,
        )
        Asteroid.containers = (
            self.asteroids,
            self.updatable,
            self.drawable,
        )
        AsteroidField.containers = self.updatable
        Shot.containers = (
            self.shots,
            self.updatable,
            self.drawable,
        )

        self.life_icons = [
            Lives(20 + i * LIFE_SPACING, 50, LIVES_RADIUS)
            for i, item in enumerate(range(PLAYER_LIVES))
        ]

        self.ship = Player(self.x, self.y, PLAYER_RADIUS)
        _asteroid_field = AsteroidField()

        self.score = 0
        self.lives = PLAYER_LIVES

        self.font = pygame.font.Font(None, 36)
        self.running = True

    def run(self) -> None:
        while self.running:
            self.handle_events()
            log_state(vars(self))
            dt = self.clock.tick(60) / 1000
            self.update(dt)
            self.check_collisions()
            self.draw()
        print("GAME OVER")
        print(f"final score: {self.score}")
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt: float) -> None:
        self.updatable.update(dt)

    def check_collisions(self) -> None:
        for asteroid in self.asteroids:
            self.player_hit(asteroid)
            for shot in self.shots:
                if not asteroid.alive():
                    break
                if shot.collides_with(asteroid):
                    points = asteroid.points
                    self.score += points
                    log_event(
                        "asteroid_shot",
                        radius=asteroid.radius,
                        points=points,
                        score=self.score,
                    )
                    asteroid.split()
                    shot.kill()

    def draw(self) -> None:
        self.screen.fill("black")
        score_surface = self.font.render(f"SCORE: {self.score}", True, "white")
        for member in self.drawable:
            member.draw(self.screen)
        for icon in self.life_icons[: self.lives]:
            icon.draw(self.screen)
        self.screen.blit(score_surface, (10, 10))
        # self.lives_group.draw(self.screen)
        pygame.display.flip()

    def player_hit(self, asteroid) -> None:
        invulnerable = self.ship.is_invulnerable
        hit = asteroid.collides_with(self.ship) and not invulnerable
        if hit:
            log_event("player_died", lives_remaining=self.lives)
            if self.lives > 1:
                self.lives -= 1
                self.ship.position = pygame.Vector2(self.x, self.y)
                self.ship.rotation = 0.0
                self.ship.invuln_timer = PLAYER_INVULN_SECONDS
            elif self.lives == 1:
                self.lives = 0
                self.running = False
