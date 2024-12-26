import pygame
import pygame.gfxdraw
from src.LEVELS import Levels
from pygame import Vector2
from src.GameConfig import GameConfig
from src.Game import Game
from src.MainMenu import MainMenu
from src.Scoreboard import Scoreboard, update_level
from src.InputManager import InputManager


class GameManager:
    def __init__(self):
        self.dt = 0
        self.running = True
        self.currentLevel = GameConfig.DEFAULT_LEVEL
        self.scroll = 0
        self.scroll_speed = GameConfig.SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.icon_img = pygame.image.load('assets/ico.png')
        self.ground_img = pygame.image.load('assets/ground.png')
        self.screen = pygame.display.set_mode(
            Vector2(GameConfig.SCREEN_DIMENSION.x, GameConfig.SCREEN_DIMENSION.y + GameConfig.GROUND_SPACE))
        self.game = Game(game_manager=self, screen=self.screen)
        self.clock = pygame.time.Clock()
        self.setup_pygame()
        self.menu = MainMenu(screen=self.screen)
        self.scoreboard = Scoreboard(screen=self.screen)

    def setup_pygame(self):
        pygame.display.set_icon(self.icon_img)
        pygame.init()
        pygame.display.set_caption(GameConfig.WINDOW_NAME)

    def start_application(self):
        print('Application Flappy_EEG starting...')
        self.game_loop()

    def game_loop(self):
        while self.running:
            InputManager.refresh_inputs()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    InputManager.handle_event(event)
            self.screen.blit(self.bg_img, (0, 0))
            match self.currentLevel:
                case Levels.GAME:
                    self.game.update(self.dt)
                    self.game.draw(self.screen)
                    pygame.display.flip()
                case Levels.MENU:
                    self.game.update_bg()
                    self.game.draw_ground(self.screen)
                    self.menu.draw(self.screen)
                case Levels.SCOREBOARD:
                    self.game.update_bg()
                    self.game.draw_ground(self.screen)
                    self.scoreboard.draw(self.screen)
                    self.scoreboard.menu.update(events)
                    self.currentLevel = update_level()
                case Levels.CONFIG:
                    #TODO
                    pass
            pygame.display.flip()
            self.dt = self.clock.tick(GameConfig.REFRESH_RATE) / 1000
        pygame.quit()

    def set_level(self, level:Levels):
        self.currentLevel = level
