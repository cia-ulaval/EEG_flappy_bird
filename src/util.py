import os
import sys

import pygame
import pygame_menu as pm
import pygame_menu.font

from src.GameConfig import GameConfig


#####################################################
# Utility python module which objective is to bring
# together functions useful services that would be
# relevant to share throughout the project
#####################################################

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def join_resource_path(path):
    return os.path.join(GameConfig.RESSOURCES_DIR, path)


def load_image(complete_path):
    return pygame.image.load(resource_path(complete_path))


def load_image_rect(complete_path, colorkey=None, rescale=None, resize=None):
    image = pygame.image.load(resource_path(complete_path))

    if rescale:
        size = image.get_size()
        size = (size[0] * rescale.x, size[1] * rescale.y)
        image = pygame.transform.scale(image, size)
    elif resize:
        image = pygame.transform.scale(image, resize)

    image = image.convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        print(f'The sound {name} is invalid')
        return NoneSound()

    rel_path = os.path.join(GameConfig.RESSOURCES_DIR, GameConfig.SOUNDS_DIR, name)
    fullpath = resource_path(rel_path)
    sound = pygame.mixer.Sound(fullpath)

    return sound


def rotate_around_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


def get_menu_theme():
    theme = pm.themes.THEME_DARK.copy()
    theme.title_bar_style = pm.widgets.MENUBAR_STYLE_NONE
    theme.background_color = pm.themes.TRANSPARENT_COLOR

    theme.widget_font = pygame_menu.font.FONT_8BIT
    theme.widget_font_color = (255, 255, 255)
    theme.widget_font_size = 30
    theme.widget_margin = (0, 20)
    theme.selection_color = (200, 100, 80)

    return theme


def get_config_value_by_screen_size(config_dict: dict):
    screen_width = GameConfig.SCREEN_DIMENSION.x
    applicable_keys = [key for key in config_dict.keys() if key <= screen_width]
    if not applicable_keys:
        return list(config_dict.values())[0]
    best_key = max(applicable_keys)
    return config_dict[best_key]
