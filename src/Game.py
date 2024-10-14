from src.Bird import Bird
from src.InputManager import InputManager
from src.GameConfig import GameConfig
from src.util import load_image
import pygame


class Game:
    def __init__(self, screen:pygame.Surface):
        self.init_variables(screen)

    def init_variables(self, screen:pygame.Surface):
        self.score = 0
        self.bird = Bird(screen)
        self.scroll = 0
        self.scroll_speed = GameConfig.SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.ground_img, _ = load_image('assets/ground.png')

        # adds all sub-objects to the render group
        self.group = pygame.sprite.RenderPlain((self.bird))
    
    def click():
        pass

    def add_score():
        pass

    def draw(self, screen):
        screen.blit(self.ground_img, (self.scroll, GameConfig.SCREEN_DIMENSION.y))
        self.group.draw(screen)

    def update(self, dt):
        # jump if space is down
        if InputManager.is_jump_down():
            self.bird.jump(dt)

        # scroll the background
        self.scroll += self.scroll_speed
        if abs(self.scroll) > 450:
            self.scroll = 0
  
        # update it's sub-objects
        self.group.update(dt)
        
