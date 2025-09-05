import pygame
import random
from collections import deque

from src import GameManager
from src.Bird import Bird
from src.Difficulty import Difficulty
from src.Pipe import Pipe
from src.InputManager import InputManager
from src.GameConfig import GameConfig
from src.Levels import Levels
from src.PipeTypes import PipeTypes
from src.util import load_image_rect, load_image, get_config_value_by_screen_size


class Game:
    def __init__(self, screen:pygame.Surface, game_manager:GameManager):
        self.initialScrollSpeed = get_config_value_by_screen_size(GameConfig.INITIAL_SCROLL_SPEEDS)
        self.scroll_speed = self.initialScrollSpeed
        self.max_scroll_speed = self.initialScrollSpeed
        self.paused = False
        self.score = 0
        self.bird = Bird(screen)
        self.scroll = 0
        self.screen = screen
        self.pipe_timer = 0
        self.difficulty_coefficient = 0
        self.pipes = pygame.sprite.Group()
        self.pipes_pool = deque()
        self.add_pipes()
        self.ground_img, _ = load_image_rect('assets/ground.png')
        self.screen_width = GameConfig.SCREEN_DIMENSION.x
        self.screen_height = GameConfig.SCREEN_DIMENSION.y
        self.ground_width = self.ground_img.get_width()
        self.pipes_active = game_manager.get_pipes_active()
        self.invincible = game_manager.get_invincibility()
        self.bg_img = pygame.transform.scale(load_image('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.bg_img, _ = load_image_rect('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.ground_img, _ = load_image_rect('assets/ground.png')
        self.group = pygame.sprite.RenderPlain((self.bird))
        self.game_manager = game_manager
        self.score_font = pygame.font.SysFont('Segoe', 26)


    def add_pipes(self):
        for _ in range(GameConfig.PIPES_BUFFER):
            self.pipes_pool.append(Pipe(0, 0, PipeTypes.UP))
            self.pipes_pool.append(Pipe(0, 0, PipeTypes.DOWN))

    def add_score(self):
        self.score += 1
        self.calculate_difficulty_values()

    def draw_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, GameConfig.FONT_COLOR)
        self.screen.blit(score_text, (10, 10))

    def draw_ground(self, screen: pygame.Surface):
        n = int((self.screen_width - self.scroll) // self.ground_width + 2)
        for i in range(n):
            x = self.scroll + i * self.ground_width
            screen.blit(self.ground_img, (x, self.screen_height - GameConfig.GROUND_SPACE))

    def draw(self, screen):
        self.pipes.draw(screen)
        self.draw_ground(screen)
        self.group.draw(screen)
        self.draw_score()

    def update_bg(self):
        self.scroll -= self.max_scroll_speed

    def update(self, dt):
        if InputManager.echap_pressed:
            self.paused = True
            self.game_manager.set_level(Levels.PAUSE_MENU)
            self.bird.reset_velocity()
            difficulty = self.game_manager.get_difficulty()
            if difficulty is Difficulty.FACILE.value:
                self.bird.reset_first_jump()
        if InputManager.is_jump_down():
            self.bird.jump()
        if (not self.invincible) and (pygame.sprite.spritecollideany(self.bird, self.pipes) or self.bird.crashed()):
            self.game_over()
        else:
            self.scroll_speed = self.max_scroll_speed
        self.update_bg()
        if not self.bird.first_jump and self.pipes_active and not self.paused:
            self.pipes.update(self.max_scroll_speed)
            self.group.update(dt)
            for pipe in list(self.pipes):
                if pipe.rect.x <= -self.screen_width:
                    self.pipes.remove(pipe)
                    self.pipes_pool.append(pipe)
                if pipe.pipe_type == PipeTypes.DOWN and not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.add_score()
            if self.pipe_timer <= 0:
                self.spawn_pipes()
                self.pipe_timer = random.randint(
                    int(75 / (1 + self.difficulty_coefficient)),
                    int(150 / (1 + self.difficulty_coefficient))
                )
            self.pipe_timer -= 1
        elif not self.bird.first_jump and not self.pipes_active:
            self.group.update(dt)

    def spawn_pipes(self):
        if len(self.pipes_pool) < 2:
            self.add_pipes()

        pipes_top = self.pipes_pool.pop()
        pipes_bottom = self.pipes_pool.pop()

        abs_min_gap = int(150 / ((1 + self.difficulty_coefficient) * 2))
        min_gap = max(int(0.20 * self.screen_height / (1 + self.difficulty_coefficient)), abs_min_gap)
        max_gap = max(int(0.35 * self.screen_height / (1 + self.difficulty_coefficient)), abs_min_gap + 30)

        abs_min_visible_height = 700
        pipe_visible_height = max(int(0.73 * self.screen_height), abs_min_visible_height)
        y_top_min = int((0.25 * (1 + (self.difficulty_coefficient / 500))) * self.screen_height) - pipe_visible_height
        y_top_max = int((0.6 / (1 + (self.difficulty_coefficient / 500))) * self.screen_height) - min_gap - pipe_visible_height

        gap_height = random.randint(min_gap, max_gap)
        y_top = random.randint(y_top_min, y_top_max)
        y_bottom = y_top + gap_height + pipe_visible_height

        pipes_top.set_pipe_type(PipeTypes.UP)
        pipes_top.set_position(self.screen_width, y_top)
        pipes_top.passed = False

        pipes_bottom.set_pipe_type(PipeTypes.DOWN)
        pipes_bottom.set_position(self.screen_width, y_bottom)
        pipes_bottom.passed = False

        self.pipes.add(pipes_top, pipes_bottom)

    def calculate_difficulty_values(self):
        difficulty = self.game_manager.get_difficulty() - 1
        if difficulty >= 0 and self.score % GameConfig.SCORES_DIFFICULTY_CHECKPOINTS[difficulty] == 0:
            if self.max_scroll_speed <= self.initialScrollSpeed + GameConfig.MAX_SCROLL_SPEED_AUGMENTATIONS[difficulty]:
                self.max_scroll_speed += GameConfig.SCROLL_SPEED_AUGMENTATIONS[difficulty]
                print(self.max_scroll_speed)
            else:
                print("Maximum scroll speed has been reached")
            if self.difficulty_coefficient <= GameConfig.MAX_DIFFICULTY_COEFFICIENTS[difficulty]:
                self.difficulty_coefficient += GameConfig.DIFFICULTY_COEFFICIENTS[difficulty]
            else:
                print("Maximum difficulty has been reached")


    def game_over(self):
        self.scroll_speed = 0
        self.max_scroll_speed = 0
        self.difficulty_coefficient = 0
        self.game_manager.record_score(self.score)
        self.game_manager.set_level(Levels.SCOREBOARD)

    def set_paused(self, paused):
        self.paused = paused
