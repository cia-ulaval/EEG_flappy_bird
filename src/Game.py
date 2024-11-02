from src import GameManager
from src.Bird import Bird
from src.InputManager import InputManager
from src.GameConfig import GameConfig
from src.LEVELS import Levels
from src.util import load_image
import pygame

class Game:
    def __init__(self, screen:pygame.Surface, game_manager:GameManager):
        self.score = 0
        self.bird = Bird(screen)
        self.scroll = 0
        self.scroll_speed = GameConfig.SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.ground_img, _ = load_image('assets/ground.png')
        self.group = pygame.sprite.RenderPlain((self.bird))
        self.game_manager = game_manager

    def click(self):
       pass

    def add_score(self):
        pass

    def draw_ground(self,screen:pygame.Surface):
        screen.blit(self.ground_img, (self.scroll, GameConfig.SCREEN_DIMENSION.y))

    def draw(self, screen):
        self.draw_ground(screen)
        self.group.draw(screen)

    def update_bg(self):
        self.scroll += self.scroll_speed
        if abs(self.scroll) > 450:
            self.scroll = 0

    def update(self, dt):
        if InputManager.is_jump_down():
            self.bird.jump(dt)
        if self.bird.crashed():
            self.scroll_speed = 0
            self.game_manager.set_level(Levels.SCOREBOARD)
        else:
            self.scroll_speed = GameConfig.SCROLL_SPEED
        self.update_bg()
        self.group.update(dt)


