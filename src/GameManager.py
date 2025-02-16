import random

import pygame
import pygame.gfxdraw

from src import Difficulty
from src.Levels import Levels
from pygame import Vector2
from src.GameConfig import GameConfig
from src.Game import Game
from src.MainMenu import MainMenu
from src.OptionsMenu import OptionsMenu
from src.Scoreboard import Scoreboard
from src.InputManager import InputManager
from src.Difficulty import Difficulty


def get_difficulty_from_value(value):
    return next((diff for diff in Difficulty if diff.value == value), None)


class GameManager:
    def __init__(self):
        pygame.init()
        self.username = "user" + str(random.randint(1000, 9999))
        self.dt = 0
        self.running = True
        self.pipes_active = True
        self.difficulty = Difficulty.FACILE.value
        self.current_level = GameConfig.DEFAULT_LEVEL
        self.scroll = 0
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.icon_img = pygame.image.load('assets/ico.png')
        self.ground_img = pygame.image.load('assets/ground.png')
        self.screen = pygame.display.set_mode(
            Vector2(GameConfig.SCREEN_DIMENSION.x, GameConfig.SCREEN_DIMENSION.y + GameConfig.GROUND_SPACE))
        self.clock = pygame.time.Clock()
        self.setup_pygame()
        self.game = Game(game_manager=self, screen=self.screen)
        self.menu = MainMenu(screen=self.screen, game_manager=self)
        self.optionsMenu = OptionsMenu(screen=self.screen, game_manager=self)
        self.scoreboard = Scoreboard(screen=self.screen, game_manager=self)

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
            match self.current_level:
                case Levels.GAME:
                    self.game.update(self.dt)
                    self.game.draw(self.screen)
                    pygame.display.flip()
                case Levels.MENU:
                    self.game.update_bg()
                    self.game.draw_ground(self.screen)
                    self.menu.menu.update(events)
                    self.menu.draw(self.screen)
                case Levels.SCOREBOARD:
                    self.game.update_bg()
                    self.game.draw_ground(self.screen)
                    self.scoreboard.menu.update(events)
                    self.scoreboard.update()
                    self.scoreboard.draw(self.screen)
                case Levels.CONFIG:
                    self.game.update_bg()
                    self.game.draw_ground(self.screen)
                    self.optionsMenu.menu.update(events)
                    self.optionsMenu.draw(self.screen)
            pygame.display.flip()
            self.dt = self.clock.tick(GameConfig.REFRESH_RATE) / 1000
        pygame.quit()

    def set_level(self, level:Levels):
        if level == Levels.GAME:
            self.game.__init__(game_manager=self, screen=self.screen)
        self.current_level = level

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def get_difficulty(self):
        return self.difficulty

    def set_pipes_active(self, pipes_active):
        self.pipes_active = pipes_active

    def get_pipes_active(self):
        return self.pipes_active

    def record_score(self, score):
        self.scoreboard.record_score(self.username, score)
        self.scoreboard = Scoreboard(screen=self.screen, game_manager=self)
        self.set_level(Levels.SCOREBOARD)
