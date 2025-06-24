import os
import sys
import pygame_menu as pm
import pygame_menu.font
from src.GameConfig import GameConfig
import pygame

#####################################################
# Utility python module which objective is to bring
# together functions useful services that would be
# relevant to share throughout the project
#####################################################

def resource_path(relative_path):
    """Returns the absolute path to the resource"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_image(complete_path):
    """
    Loads the image ressource of a given name and return it if valid.

    Returns:
        pygame.Surface.
    """
    return pygame.image.load(resource_path(complete_path))

def load_image_rect(complete_path, colorkey=None, rescale:pygame.Vector2=None, resize:pygame.Vector2=None) -> tuple[pygame.Surface, pygame.Rect]:
    """
    Loads the image ressource of a given name, scale it and recolor it
    if specified.

    Args:
        name (String): Name of the image file
        colorkey (Color | int, optional): Sets colorkey for transparency. Defaults to None.
        rescale (pygame.Vector2, optional): Scaling of the object. Defaults to None, change it to trigger it.
        resize (pygame.Vector2, optional): Resizing the image. Defaults to None, change it to trigger it.

    Returns:
        pygame.Surface, pygame.Rect: Loaded image.
    """
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
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    return image, image.get_rect()

def load_sound(name):
    """
    Load a sound according to the filename given and return it if valid.
    Args:
        name (String): Filename of the sound.
    Returns:
        pygame.mixer.Sound: Pygame sound.
    """
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        print(f'The sound {name} is invalid')
        return NoneSound()

    fullpath = os.path.join(GameConfig.SRC_DIR,
                            GameConfig.RESSOURCES_DIR,
                            GameConfig.SOUNDS_DIR,
                            name)
    sound = pygame.mixer.Sound(fullpath)

    return sound

def rotate_around_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x,y)).center)
    return rotated_image, new_rect

def get_menu_theme():
    theme = pm.themes.THEME_DARK.copy()
    theme.title_bar_style = pm.widgets.MENUBAR_STYLE_NONE
    theme.background_color = pm.themes.TRANSPARENT_COLOR

    theme.widget_font = pygame_menu.font.FONT_8BIT
    theme.widget_font_color = (255, 255, 255)
    theme.widget_font_size = 30

    theme.selection_color = (200, 100, 80)
    theme.widget_margin = (0, 20)
    return theme