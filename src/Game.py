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
from src.util import load_image
import pygame

class Game:
    def __init__(self, screen:pygame.Surface, game_manager:GameManager):
        self.score = 0
        self.bird = Bird(screen)
        self.scroll = 0
        self.screen = screen
        self.pipe_timer = 0
        self.difficulty_coefficient = 0
        self.pipes = pygame.sprite.Group()
        self.pipes_pool = deque()
        self.add_pipes()
        self.scroll_speed = GameConfig.INITIAL_SCROLL_SPEED
        self.max_scroll_speed = GameConfig.INITIAL_SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.ground_img, _ = load_image('assets/ground.png')
        self.group = pygame.sprite.RenderPlain((self.bird))
        self.game_manager = game_manager
        self.font = pygame.font.SysFont('Segoe', 26)

    def add_pipes(self, initial_count=GameConfig.PIPES_BUFFER):
        for _ in range(initial_count):
            self.pipes_pool.append(Pipe(self.screen, 0, 0, PipeTypes.UP))
            self.pipes_pool.append(Pipe(self.screen, 0, 0, PipeTypes.DOWN))


    def click(self):
       pass

    def add_score(self):
        self.score += 1
        self.calculate_difficulty_values()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))  # White text
        self.screen.blit(score_text, (10, 10))

    def draw_ground(self,screen:pygame.Surface):
        screen.blit(self.ground_img, (self.scroll, GameConfig.SCREEN_DIMENSION.y))

    def draw(self, screen):
        self.pipes.draw(screen)
        self.draw_ground(screen)
        self.group.draw(screen)
        self.draw_score()

    def update_bg(self):
        self.scroll += self.max_scroll_speed
        if abs(self.scroll) > 450:
            self.scroll = 0

    def update(self, dt):
        pipes_active = self.game_manager.get_pipes_active()
        if InputManager.echap_pressed:
            self.game_manager.set_level(Levels.PAUSE_MENU)
            self.bird.reset_velocity()
            difficulty = self.game_manager.get_difficulty()
            if difficulty is Difficulty.FACILE.value:
                self.bird.reset_first_jump()
        if InputManager.is_jump_down():
            self.bird.jump(dt)
        if any(pipe.rect.colliderect(self.bird.collision_rect) for pipe in self.pipes) | self.bird.crashed():
            self.game_over()
        else:
            self.scroll_speed = self.max_scroll_speed
        self.update_bg()
        if not self.bird.first_jump and pipes_active:
            self.pipes.update(self.max_scroll_speed)
            self.group.update(dt)
            for pipe in self.pipes:
                if pipe.rect.x <= -GameConfig.SCREEN_DIMENSION.x:
                    self.pipes.remove(pipe)
                    self.pipes_pool.append(pipe)
                if pipe.pipe_type == PipeTypes.DOWN and not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.add_score()
            if self.pipe_timer <= 0:
                self.spawn_pipes()
                self.pipe_timer = random.randint(int(75 / (1 + self.difficulty_coefficient)), int(150 / (1 + self.difficulty_coefficient)))
            self.pipe_timer -= 1
            
        elif not self.bird.first_jump and not pipes_active:
            self.group.update(dt)

    def spawn_pipes(self):
        if len(self.pipes_pool) < 2:
            self.add_pipes()

        pipes_top = self.pipes_pool.pop()
        pipes_bottom = self.pipes_pool.pop()

        screen_width = GameConfig.SCREEN_DIMENSION[0]
        gap_height = random.randint(int(100 / (1 + self.difficulty_coefficient)),
                                    int(200 / (1 + self.difficulty_coefficient)))
        y_top = random.randint(-500, -325)
        y_bottom = y_top + gap_height + 700

        pipes_top.set_pipe_type(PipeTypes.UP)
        pipes_top.set_position(screen_width, y_top)
        pipes_top.passed = False

        pipes_bottom.set_pipe_type(PipeTypes.DOWN)
        pipes_bottom.set_position(screen_width, y_bottom)
        pipes_bottom.passed = False

        self.pipes.add(pipes_top, pipes_bottom)

    def calculate_difficulty_values(self):
        difficulty = self.game_manager.get_difficulty()
        if difficulty != 0 and self.score % GameConfig.SCORES_DIFFICULTY_CHECKPOINTS[difficulty - 1] == 0:
            if self.max_scroll_speed <= GameConfig.MAX_SCROLL_SPEED_AUGMENTATIONS[difficulty - 1]:
                self.max_scroll_speed -= GameConfig.SCROLL_SPEED_AUGMENTATIONS[difficulty - 1]
            else:
                print("Maximum scroll speed has been reached")
            if self.difficulty_coefficient <= GameConfig.MAX_DIFFICULTY_COEFFICIENTS[difficulty - 1]:
                self.difficulty_coefficient += GameConfig.DIFFICULTY_COEFFICIENTS[difficulty - 1]
            else:
                print("Maximum difficulty has been reached")


    def game_over(self):
        self.scroll_speed = 0
        self.max_scroll_speed = 0
        self.difficulty_coefficient = 0
        self.game_manager.record_score(self.score)
        self.game_manager.set_level(Levels.SCOREBOARD)





