
import pygame_menu as pm
import json
import pygame
from math import log10

import pygame_menu.font
from src.InputManager import InputManager
from src.util import load_image
from src.GameConfig import GameConfig
from src.LEVELS import Levels
class Scoreboard:


    #créer le constructeur
    def __init__(self, screen:pygame.Surface):
        self.data = json.load(open("data/scores.json"))


        self.init_variables()

    #initialiser les variables
    def init_variables(self):

        # créer le thème
        theme = pm.themes.THEME_SOLARIZED.copy()
        theme.title_bar_style = pm.widgets.MENUBAR_STYLE_NONE
        theme.background_color = (0, 0, 255, 0)


        # loader le background
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)


        # loader le background du scoreboard
        self.leaderboard = pygame.transform.scale(pygame.image.load('assets/bgScoreboard.png'), GameConfig.SCREEN_DIMENSION)
        self.leaderboard, _ = load_image('assets/bgScoreboard.png',
                                         resize=(GameConfig.SCREEN_DIMENSION[0]-200,GameConfig.SCREEN_DIMENSION[1]-50))


        #créer le menu
        self.menu = pm.Menu(width=GameConfig.SCREEN_DIMENSION[0]-200,
                       height=GameConfig.SCREEN_DIMENSION[1]-100,
                       theme=theme,
                       title="")
        self.menu.set_relative_position(50, 55)


        #mettre le label de l'écriture scoreboard
        self.menu.add.label(title="Scoreboard\n\n", font_size=40, font_color=(255, 255, 255)
                                    , font_name=pygame_menu.font.FONT_8BIT)


        #mettre les indentations pour que chaque
        indentIndex = int(log10(len(self.data.values()))) + 1
        indentNom = max(list(map(lambda e: len(e["nom"][:18]), list(self.data.values())))) + 1

        #ajouter chaque élément
        for index, item in enumerate(sorted(list(self.data.values()), key=lambda x: x["score"], reverse=True)):
            self.menu.add.label(title=f"{index+1:<{indentIndex}}"
                                      f"{item["nom"][:15]:^{indentNom}}"
                                      f"{item["score"]:>4}\n",
                    font_color=[(183, 183, 3 ), (111, 111, 111), (147, 105, 50),(0, 0, 0)][min(index, 3)],
                    font_name='assets/policeFlappy.ttf',
                                        font_size=20)


    #dessiner tous les éléments du menu
    def draw(self, screen):
        screen.blit(self.bg_img, (0, 0))

        self.draw_scoreboard(screen)
        self.menu.draw(screen)


    #dessiner le background du scoreboard
    def draw_scoreboard(self, screen):
        screen.blit(self.leaderboard, (100, 50))

    #fonction pour savoir s'il faut changer de
    def updateLevel(self):
        if InputManager.echap_pressed:
            return Levels.MENU
        else:
            return Levels.SCOREBOARD

