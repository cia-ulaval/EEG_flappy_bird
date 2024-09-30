import os
from src.GameConfig import GameConfig
import pygame

#####################################################
# Module python utilitaire 
# dont l'objectif est de regrouper des fonctions
# utiles dont il serait pertinent de partager dans tout le projet!
#####################################################

def load_image(complete_path, colorkey=None, rescale:pygame.Vector2=None, resize:pygame.Vector2=None):
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
    # load the image
    image = pygame.image.load(complete_path)

    # resize it
    if rescale:
        size = image.get_size()
        size = (size[0] * rescale.x, size[1] * rescale.y)
        image = pygame.transform.scale(image, size)
    elif resize:
        image = pygame.transform.scale(image, resize)

    # convert the image into a pygame.Surface
    image = image.convert()

    # setting the colorkey
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
    # class to prevent errors if name is invalid
    class NoneSound:
        def play(self):
            pass

    # return the NoneSound if the name of the sound is invalid
    if not pygame.mixer or not pygame.mixer.get_init():
        print(f'The sound {name} is invalid')
        return NoneSound()

    # creation du son
    fullpath = os.path.join(GameConfig.SRC_DIR,
                            GameConfig.RESSOURCES_DIR,
                            GameConfig.SOUNDS_DIR,
                            name)
    sound = pygame.mixer.Sound(fullpath)

    return sound