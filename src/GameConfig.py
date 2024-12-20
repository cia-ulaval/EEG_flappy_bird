from pygame import Vector2
from src.LEVELS import Levels

class GameConfig:
    SCREEN_DIMENSION = Vector2(800, 600)
    WINDOW_NAME = "Flappy Brain"
    REFRESH_RATE = 60
    SCROLL_SPEED = -6
    GROUND_SPACE = 50
    DEFAULT_LEVEL = Levels.GAME
    GRAVITY_FORCE = 3000
    FONT = 'assets/policeFlappy.ttf'
    FLAP_ANIMATION_TIMING = 100