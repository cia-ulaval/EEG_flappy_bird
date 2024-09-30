import pygame
import pygame.gfxdraw
from pygame import Vector2

from src.Bird import Bird
from src.GameConfig import GameConfig
from src.Game import Game
from src.InputManager import InputManager


class GameManager:

    def __init__(self):
        self.setup_pygame()
        self.init_variables()


    def init_variables(self):
        self.dt = 0
        self.running = True
        self.scroll = 0
        self.scroll_speed = GameConfig.SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.ground_img = pygame.image.load('assets/ground.png')
        self.game = Game(screen=self.screen)

    def setup_pygame(self):
        pygame.init()
        pygame.display.set_caption(GameConfig.WINDOW_NAME)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Vector2(GameConfig.SCREEN_DIMENSION.x, GameConfig.SCREEN_DIMENSION.y +GameConfig.GROUND_SPACE))

    def start_application(self):
        print('Application Flappy_EEG starting...')
        self.game_loop()

    def game_loop(self):
        # Main game loop
        while self.running:

            # Refresh all inputs of the last frame
            InputManager.refresh_inputs()

            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    InputManager.handle_event(event)
                
            # clear the screen buffer with a color
            self.screen.blit(self.bg_img, (0, 0))
            
            self.game.update(self.dt)
            self.game.draw(self.screen)

            # flip() to make the drawing appear on screen
            pygame.display.flip()

            # clock to limit loop to the refresh rate
            self.dt = self.clock.tick(GameConfig.REFRESH_RATE) / 1000

        pygame.quit()
