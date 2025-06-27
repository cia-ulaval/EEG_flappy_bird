import math

import pygame_menu as pm
import json
import pygame
import pygame_menu.font
from src.InputManager import InputManager
from src.util import load_image_rect, get_menu_theme, load_image, resource_path
from src.GameConfig import GameConfig
from src import GameManager
from src.Levels import Levels

class Scoreboard:
    def __init__(self, screen:pygame.Surface, game_manager: GameManager):
        self.game_manager = game_manager
        self.file = open("data/scores.json")
        self.data = json.load(self.file)
        self.GOLD = (191, 150, 37)
        self.SILVER = (138, 158, 163)
        self.BRONZE = (177, 89, 26)

        self.theme = pm.themes.THEME_SOLARIZED.copy()
        self.bg_img = pygame.transform.scale(load_image('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.leaderboard = pygame.transform.scale(load_image('assets/bgScoreboard.png'),
                                                  GameConfig.SCREEN_DIMENSION)
        self.create_theme()
        self.menu = pm.Menu(width=GameConfig.SCREEN_DIMENSION[0] - 200,
                            height=GameConfig.SCREEN_DIMENSION[1] - 100,
                            theme=self.theme,
                            title="")

        self.create_menu()
        self.resize_components()
        self.add_games_to_leaderboard()
        self.add_return_button()

    def create_theme(self):
        self.theme = get_menu_theme()

    def resize_components(self):
        self.bg_img, _ = load_image_rect('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.leaderboard, _ = load_image_rect('assets/bgScoreboard.png',
                                              resize=(GameConfig.SCREEN_DIMENSION[0] - 200, GameConfig.SCREEN_DIMENSION[1] - 50))

    def create_menu(self):
        self.menu.set_relative_position(50, 55)
        self.menu.add.label(title="Pointages\n\n", font_size=GameConfig.MENU_FONT_TILE_SIZE, font_color=GameConfig.FONT_COLOR_SECONDARY,
                            font_name=pygame_menu.font.FONT_8BIT)

    def add_games_to_leaderboard(self):
        indent_index = self.indent_score_indexes()
        indent_names = self.indent_score_names()

        sorted_data = sorted(self.data.items(), key=lambda x: x[1], reverse=True)

        position = 1
        for index, (name, score) in enumerate(sorted_data):
            self.menu.add.label(
                title=f"{position:<{indent_index}} {name:^{indent_names}} {score:>4}",
                font_color=[self.GOLD, self.SILVER, self.BRONZE, GameConfig.FONT_COLOR][min(index, 3)],
                font_name=GameConfig.FONT,
                font_size=GameConfig.MENU_FONT_P_SIZE,
                margin=(0, 15)
            )
            position += 1

    def indent_score_indexes(self):
        return int(math.log10(len(self.data))) + 1 if len(self.data) > 1 else 1

    def indent_score_names(self):
        return max(len(name) for name in self.data.keys())

    def add_return_button(self):
        self.menu.add.button(title="Retour", font_size=GameConfig.MENU_FONT_P_SIZE, font_color=GameConfig.FONT_COLOR,
                                    font_name=pygame_menu.font.FONT_8BIT, action=lambda: self.set_level(Levels.MENU),
                                    background_color=None, border_width=0)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 64))
        screen.blit(overlay, (0, 0))

        self.draw_scoreboard(screen)
        self.menu.draw(screen)

    def draw_scoreboard(self, screen):
        screen.blit(self.leaderboard, (100, 50))

    def update(self):
        if InputManager.echap_pressed:
            self.set_level(Levels.MENU)

    def set_level(self, level):
        self.game_manager.set_level(level)

    def record_score(self, username, score):
        if username not in self.data.keys() or self.data[username] < score:
            self.data[username] = score
            self.write_new_scores()

    def write_new_scores(self):
        with open(resource_path("data/scores.json"), 'w+') as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)