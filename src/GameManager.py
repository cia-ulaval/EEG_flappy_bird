import pygame
import pygame.gfxdraw
import math
from src.GameConfig import GameConfig
class GameManager:
    
    def __init__(self):
        self.init_variables()
        self.setup_pygame()
    
    def init_variables(self):
        pass
    
    def setup_pygame(self):
        pygame.init()
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
            t = pygame.time.get_ticks()
            longueur_onde = 500
            color = (255, 0, 255)
            x = self.screen.get_width()/2 + math.sin(t/longueur_onde) * 100
            y = self.screen.get_height()/2 + math.cos(t/longueur_onde) * 100
            position = pygame.Vector2(x,y)
            pygame.gfxdraw.aacircle(self.screen, int(x),int(y), 30,color)
            pygame.gfxdraw.filled_circle(self.screen, int(x),int(y), 30, color)
            
            # flip() to make the drawing appear on screen
            pygame.display.flip()
            
            # clock to limit loop to 60 frames/second
            self.dt = self.clock.tick(60) / 1000
        
        pygame.quit