import pygame_menu as pm
import pygame
import pygame_menu.font

from src import GameManager
from src.Difficulty import Difficulty
from src.util import load_image_rect, get_menu_theme, load_image
from src.GameConfig import GameConfig
from src.Levels import Levels


def set_sound_level(sound_level):
    volume = sound_level / 100
    pygame.mixer.music.set_volume(volume)


def format_difficulties():
    difficulty = sorted(
        [(name, value.value) for name, value in Difficulty.__members__.items()],
        key=lambda x: x[1]
    )
    return difficulty


class OptionsMenu:
    def __init__(self, screen:pygame.Surface, game_manager: GameManager):
        self.screen = screen
        self.game_manager = game_manager
        self.theme = pm.themes.THEME_SOLARIZED.copy()
        self.bg_img = pygame.transform.scale(load_image('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
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
        self.bg_img, _ = load_image_rect('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)

    def create_menu(self):
        self.menu.set_relative_position(50, 55)
        self.menu.add.label(title="Options\n", font_size=GameConfig.MENU_FONT_TILE_SIZE, font_color=GameConfig.FONT_COLOR,
                            font_name=pygame_menu.font.FONT_8BIT)
        self.menu.add.text_input(title="Nom   ", textinput_id="user_input", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                                font_name=pygame_menu.font.FONT_8BIT, onchange=self.set_username,
                                background_color=None, border_width=0, maxchar=10, default=self.game_manager.get_username())
        self.menu.add.dropselect(title="Difficulte", font_size=GameConfig.MENU_FONT_P_SIZE,
                                 font_color=GameConfig.FONT_COLOR, items=format_difficulties(),
                                 font_name=pygame_menu.font.FONT_8BIT, onchange=self.set_difficulty,
                                 background_color=None, border_width=0, default=0)
        self.menu.add.toggle_switch(title="Tuyaux", font_size=GameConfig.MENU_FONT_P_SIZE,
                                 font_color=GameConfig.FONT_COLOR,
                                 font_name=pygame_menu.font.FONT_8BIT, onchange=self.set_pipes_active,
                                 default=True, background_color=None, border_width=0)
        self.menu.add.toggle_switch(title="Invincibilite", font_size=GameConfig.MENU_FONT_P_SIZE,
                                    font_color=GameConfig.FONT_COLOR,
                                    font_name=pygame_menu.font.FONT_8BIT, onchange=self.set_invincibility,
                                    default=True, background_color=None, border_width=0)
        self.menu.add.range_slider(title="Son", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                                   font_name=pygame_menu.font.FONT_8BIT, onchange=set_sound_level,
                                   range_values=[0, 100], default=50, background_color=None, border_width=0, increment=1)
        self.menu.add.button(title="Retour", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                             font_name=pygame_menu.font.FONT_8BIT, action=lambda: self.set_level(Levels.MENU), background_color=None, border_width=0)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 64))
        screen.blit(overlay, (0, 0))
        self.menu.draw(screen)

    def set_level(self, level):
        self.game_manager.set_level(level)

    def set_username(self, username):
        self.game_manager.set_username(username)

    def set_difficulty(self, selected, difficulty):
        self.game_manager.set_difficulty(difficulty)

    def set_pipes_active(self, pipes_active):
        self.game_manager.set_pipes_active(pipes_active)

    def set_invincibility(self, invincible):
        self.game_manager.set_invincibility(invincible)