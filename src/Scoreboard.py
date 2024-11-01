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


class Scoreboard:
    def __init__(self, screen:pygame.Surface):
        self.data = json.load(open("data/scores.json"))
        self.GOLD = (191, 150, 37)
        self.SILVER = (138, 158, 163)
        self.BRONZE = (177, 89, 26)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.SCOREBOARD_FONT_TILE_SIZE = 40
        self.SCOREBOARD_FONT_P_SIZE = 20
        self.theme = pm.themes.THEME_SOLARIZED.copy()
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.leaderboard = pygame.transform.scale(pygame.image.load('assets/bgScoreboard.png'),
                                                  GameConfig.SCREEN_DIMENSION)
        self.menu = pm.Menu(width=GameConfig.SCREEN_DIMENSION[0] - 200,
                            height=GameConfig.SCREEN_DIMENSION[1] - 100,
                            theme=self.theme,
                            title="")

        self.create_theme()
        self.create_menu()
        self.resize_components()
        self.add_games_to_leaderboard()

    def create_theme(self):
        self.theme.title_bar_style = pm.widgets.MENUBAR_STYLE_NONE
        self.theme.background_color = (0, 0, 255, 0)


    def resize_components(self):
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.leaderboard, _ = load_image('assets/bgScoreboard.png',
                                         resize=(GameConfig.SCREEN_DIMENSION[0] - 200, GameConfig.SCREEN_DIMENSION[1] - 50))


    def create_menu(self):
        self.menu.set_relative_position(50, 55)
        self.menu.add.label(title="Scoreboard\n\n", font_size=self.SCOREBOARD_FONT_TILE_SIZE, font_color=self.BLACK,
                            font_name=pygame_menu.font.FONT_8BIT)


    def indent_score_indexes(self):
        return int(log10(len(self.data.values()))) + 1

    def indent_score_names(self):
        return max(list(map(lambda e: len(e["nom"][:18]), list(self.data.values())))) + 1

    def add_games_to_leaderboard(self):
        indent_index = self.indent_score_indexes()
        indent_names = self.indent_score_names()
        for index, item in enumerate(sorted(list(self.data.values()), key=lambda x: x["score"], reverse=True)):
            self.menu.add.label(title=f"{index+1:<{indent_index}}"
                                      f"{item['nom'][:15]:^{indent_names}}"
                                      f"{item['score']:>4}\n",
                    font_color=[self.GOLD, self.SILVER, self.BRONZE, self.BLACK][min(index, 3)],
                    font_name=GameConfig.FONT,
                                        font_size=self.SCOREBOARD_FONT_P_SIZE)


    def draw(self, screen):
        screen.blit(self.bg_img, (0, 0))

        self.draw_scoreboard(screen)
        self.menu.draw(screen)


    def draw_scoreboard(self, screen):
        screen.blit(self.leaderboard, (100, 50))

