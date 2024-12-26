import pygame_menu as pm
import json
import pygame
from math import log10

import pygame_menu.font
from src.InputManager import InputManager
from src.util import load_image
from src.GameConfig import GameConfig
from src.LEVELS import Levels


def update_level():
    if InputManager.echap_pressed:
        return Levels.MENU
    else:
        return Levels.SCOREBOARD

class MainMenu:
    def __init__(self, screen:pygame.Surface):
        self.MENU_FONT_TILE_SIZE = 40
        self.MENU_FONT_P_SIZE = 20
        self.theme = pm.themes.THEME_SOLARIZED.copy()
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.menu = pm.Menu(width=GameConfig.SCREEN_DIMENSION[0] - 200,
                            height=GameConfig.SCREEN_DIMENSION[1] - 100,
                            theme=self.theme,
                            title="")

        self.create_theme()
        self.create_menu()
        self.resize_components()

    def create_theme(self):
        self.theme.title_bar_style = pm.widgets.MENUBAR_STYLE_NONE
        self.theme.background_color = (0, 0, 255, 0)

    def resize_components(self):
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)

    def create_menu(self):
        self.menu.set_relative_position(50, 55)
        self.menu.add.label(title="Flappy Bird EEG\n\n", font_size=self.MENU_FONT_TILE_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)
        self.menu.add.label(title="Commencer\n\n", font_size=self.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)
        self.menu.add.label(title="Options\n\n", font_size=self.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)
        self.menu.add.label(title="Options\n\n", font_size=self.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)

    def draw(self, screen):
        screen.blit(self.bg_img, (0, 0))
        self.menu.draw(screen)