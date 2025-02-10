from pygame import Vector2
from src.LEVELS import Levels

class GameConfig:
    SCREEN_DIMENSION = Vector2(800, 600)
    WINDOW_NAME = "Flappy Brain"
    REFRESH_RATE = 60
    SCROLL_SPEED = -6
    GROUND_SPACE = 50
    DEFAULT_LEVEL = Levels.NOPIPE
    GRAVITY_FORCE = 3000
    FONT = 'assets/policeFlappy.ttf'
    FONT_COLOR = (0, 0, 0)
    FLAP_ANIMATION_TIMING = 100
    MENU_FONT_TILE_SIZE = 40
    MENU_FONT_P_SIZE = 20