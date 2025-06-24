import pygame
from pygame import Vector2
from src.Levels import Levels

class GameConfig:
    SCREEN_DIMENSION = Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h)
    WINDOW_NAME = "Flappy Brain"
    REFRESH_RATE = 60
    INITIAL_SCROLL_SPEED = -4
    GROUND_SPACE = 50
    DEFAULT_LEVEL = Levels.MENU
    GRAVITY_FORCE = 3000
    MENU_FONT_TILE_SIZE = 40
    MENU_FONT_P_SIZE = 20
    FONT = 'assets/policeFlappy.ttf'
    FONT_COLOR = (255, 255, 255)
    FONT_COLOR_SECONDARY = (0, 0, 0)
    FLAP_ANIMATION_TIMING = 100
    PIPES_BUFFER = 15
    MAX_SCROLL_SPEED_AUGMENTATIONS = [0.75, 1, 4]
    SCROLL_SPEED_AUGMENTATIONS = [0.05, 0.1, 0.2]
    DIFFICULTY_COEFFICIENTS = [0.05, 0.2, 0.1]
    MAX_DIFFICULTY_COEFFICIENTS = [1, 1.75, 3]
    SCORES_DIFFICULTY_CHECKPOINTS = [1, 1, 1]