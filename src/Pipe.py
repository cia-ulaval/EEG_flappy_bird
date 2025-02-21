import pygame

from src.GameConfig import GameConfig
from src.PipeTypes import PipeTypes
from src.util import load_image

class Pipe(pygame.sprite.Sprite):
    pipe_up_image, pipe_up_rect = None, None
    pipe_down_image, pipe_down_rect = None, None

    def __init__(self, screen: pygame.Surface, x: int, y: int, pipe_type: PipeTypes):
        pygame.sprite.Sprite.__init__(self)
        self.rect, self.image, self.pipe_type = None, None, None
        if Pipe.pipe_up_image is None:
            Pipe.pipe_up_image, Pipe.pipe_up_rect = load_image("assets/pipeUp.png", -1)
            Pipe.pipe_down_image, Pipe.pipe_down_rect = load_image("assets/pipeDown.png", -1)

        self.set_pipe_type(pipe_type)
        self.rect.x, self.rect.y = x, y
        self.passed = False

    def set_position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y

    def set_pipe_type(self, pipe_type: PipeTypes):
        self.pipe_type = pipe_type
        if pipe_type == PipeTypes.UP:
            self.image = Pipe.pipe_up_image
            self.rect = Pipe.pipe_up_rect.copy()
        else:
            self.image = Pipe.pipe_down_image
            self.rect = Pipe.pipe_down_rect.copy()

    def update(self, current_scroll_speed: float):
        self.rect.x += current_scroll_speed




