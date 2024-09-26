import pygame
import pygame.gfxdraw
from pygame import Vector2

from src.Bird import Bird
from src.GameConfig import GameConfig


class GameManager:

    def __init__(self):
        self.dt = 0
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Vector2(GameConfig.SCREEN_DIMENSION.x, GameConfig.SCREEN_DIMENSION.y +GameConfig.GROUND_SPACE))
        self.scroll = 0
        self.scroll_speed = GameConfig.SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.ground_img = pygame.image.load('assets/ground.png')
        self.bird = Bird()
        self.setup_pygame()

    @staticmethod
    def setup_pygame():
        pygame.init()
        pygame.display.set_caption(GameConfig.WINDOW_NAME)

    def start_application(self):
        print('Application Flappy_EEG starting...')
        self.game_loop()

    def game_loop(self):
        # Main game loop
        while self.running:

            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # clear the screen buffer with a color
            self.screen.blit(self.bg_img, (0, 0))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.bird.jump(self.dt)

            if self.bird.position.y <= 0:
                self.bird.position.y = 0

            self.bird.position.y += self.dt * 100

            self.bird.draw(self.screen)

            self.screen.blit(self.ground_img, (self.scroll, GameConfig.SCREEN_DIMENSION.y))

            self.scroll += self.scroll_speed
            if abs(self.scroll) > 35:
                self.scroll = 0

            # flip() to make the drawing appear on screen
            pygame.display.flip()

            # clock to limit loop to the refresh rate
            self.dt = self.clock.tick(GameConfig.REFRESH_RATE) / 1000

        pygame.quit()
