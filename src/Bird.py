import pygame

from src.GameConfig import GameConfig


class Bird:
    def __init__(self):
        self.collisions = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(GameConfig.SCREEN_DIMENSION.x / 2, GameConfig.SCREEN_DIMENSION.y / 2)
        self.velocity = pygame.Vector2(0, 0)

    def jump(self, dt):
        self.position.y -= 1000 * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.position, 40)
