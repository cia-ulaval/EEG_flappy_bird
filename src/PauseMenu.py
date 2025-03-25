import pygame_menu as pm
import pygame
import pygame_menu.font

from src import GameManager
from src.InputManager import InputManager
from src.util import load_image, get_menu_theme
from src.GameConfig import GameConfig
from src.Levels import Levels


class PauseMenu:
    def __init__(self, screen:pygame.Surface, game_manager: GameManager):
        self.game_manager = game_manager

        self.screen = screen
        self.game_manager = game_manager
        self.theme = pm.themes.THEME_SOLARIZED.copy()
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.create_theme()
        self.menu = pm.Menu(width=GameConfig.SCREEN_DIMENSION[0] - 200,
                            height=GameConfig.SCREEN_DIMENSION[1] - 100,
                            theme=self.theme,
                            title="")
        self.create_menu()
        self.resize_components()

    def create_theme(self):
        self.theme = get_menu_theme()

    def resize_components(self):
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)

    def create_menu(self):
        self.menu.set_relative_position(50, 55)
        self.menu.add.label(title="Pause\n\n", font_size=GameConfig.MENU_FONT_TILE_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)
        self.menu.add.button(title="Reprendre", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                             font_name=pygame_menu.font.FONT_8BIT, action=lambda: self.set_level(Levels.GAME, True),
                             background_color=None, border_width=0)
        self.menu.add.button(title="Retour au menu", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                             font_name=pygame_menu.font.FONT_8BIT, action=lambda: self.set_level(Levels.MENU),
                             background_color=None, border_width=0)
        self.menu.add.button(title="Quitter", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                             font_name=pygame_menu.font.FONT_8BIT, action=lambda: pygame.quit(),
                             background_color=None, border_width=0)

    def update(self):
        if InputManager.echap_pressed:
            self.set_level(Levels.GAME)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        self.menu.draw(screen)

    def set_level(self, level, in_game=False):
        self.game_manager.set_level(level, in_game)
