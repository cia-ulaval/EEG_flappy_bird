import pygame
import pygame.gfxdraw
import math
from src.GameConfig import GameConfig
from src.Game import Game
class GameManager:
    def __init__(self):
        self.setup_pygame()
        self.init_variables()
    
    def init_variables(self):
        self.game = Game(screen=self.screen)
    
    def setup_pygame(self):
        pygame.init()
        pygame.display.set_caption(GameConfig.WINDOW_NAME)
        self.screen = pygame.display.set_mode(GameConfig.SCREEN_DIMENSION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
    
    def start_application(self):
        print('Application Flappy_EEG starting...')
        self.game_loop()
    
    def game_loop(self):
        # Main game loop
        while self.running:
            
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # clear the screen buffer with a color
            self.screen.fill("green")
            
            ###
            # The game render take place here
            ###
            self.game.update()
            self.game.draw(self.screen)
            
            # flip() to make the drawing appear on screen
            pygame.display.flip()
            
            # clock to limit loop to 60 frames/second
            self.dt = self.clock.tick(60) / 1000
        
        pygame.quit