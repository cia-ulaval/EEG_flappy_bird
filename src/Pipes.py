import pygame

from src.GameConfig import GameConfig
from src.util import load_image, rotate_around_center

class Pipes(pygame.sprite.Sprite):


    def __init__(self, screen: pygame.Surface, x: int, y: int, pipe_type: str):

        pygame.sprite.Sprite.__init__(self)

        if pipe_type == "up":
            self.image, self.rect = load_image("assets/pipeUp.png", -1)
        elif pipe_type == "down":
            self.image, self.rect = load_image("assets/pipeDown.png", -1)

        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        #print(self.rect)
        self.rect.x += GameConfig.SCROLL_SPEED
        if self.rect.x <= -GameConfig.SCREEN_DIMENSION.x:
            self.kill()




