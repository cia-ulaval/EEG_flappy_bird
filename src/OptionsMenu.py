import pygame_menu as pm
import pygame
import pygame_menu.font

from src.util import load_image
from src.GameConfig import GameConfig
from src.LEVELS import Levels

class OptionsMenu:
    def __init__(self, screen:pygame.Surface, game_manager):
        from src.GameManager import GameManager
        self.game_manager: GameManager = game_manager

        self.screen = screen
        self.game_manager = game_manager
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
        self.menu.add.label(title="Options\n\n", font_size=GameConfig.MENU_FONT_TILE_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)
        self.menu.add.range_slider(title="Son", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                                   font_name=pygame_menu.font.FONT_8BIT, onchange=lambda: self.set_level(Levels.CONFIG),
                                   range_values=[0, 100], default=50, background_color=None, border_width=0, increment=1)
        self.menu.add.button(title="Retour", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                             font_name=pygame_menu.font.FONT_8BIT, action=lambda: self.set_level(Levels.MENU), background_color=None, border_width=0)

    def draw(self, screen):
        screen.blit(self.bg_img, (0, 0))
        self.menu.draw(screen)

    def set_level(self, level):
        self.game_manager.set_level(level)

    def set_sound_level(self, sound_level):
        self.game_manager.set_sound_level(sound_level)
