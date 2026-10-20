from asteroids.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from asteroids.game import Game


def main() -> None:
    print("Starting Asteroids")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
