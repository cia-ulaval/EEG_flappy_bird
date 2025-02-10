import random

from src import GameManager
from src.Bird import Bird
from src.Pipes import Pipes
from src.InputManager import InputManager
from src.GameConfig import GameConfig
from src.LEVELS import Levels
from src.util import load_image
import pygame

class Game:
    def __init__(self, screen:pygame.Surface, game_manager:GameManager):
        self.score = 0
        self.bird = Bird(screen)
        self.scroll = 0
        self.screen = screen
        self.pipe_timer = 0
        self.pipes = pygame.sprite.Group()
        self.scroll_speed = GameConfig.SCROLL_SPEED
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), GameConfig.SCREEN_DIMENSION)
        self.bg_img, _ = load_image('assets/bg.png', resize=GameConfig.SCREEN_DIMENSION)
        self.ground_img, _ = load_image('assets/ground.png')
        self.group = pygame.sprite.RenderPlain((self.bird))
        self.game_manager = game_manager
        self.font = pygame.font.SysFont('Segoe', 26)

    def click(self):
       pass

    def add_score(self):
        self.score += 1
        print(f"Score: {self.score}")

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
        self.scroll += self.scroll_speed
        if abs(self.scroll) > 450:
            self.scroll = 0

    def update(self, dt):
        if InputManager.is_jump_down():
            self.bird.jump(dt)
        if any(pipe.rect.colliderect(self.bird.collision_rect) for pipe in self.pipes) | self.bird.crashed():
            self.game_over()
        else:
            self.scroll_speed = GameConfig.SCROLL_SPEED
        self.update_bg()
        if not self.bird.first_jump:
            self.pipes.update()
            self.group.update(dt)
            for pipe in self.pipes:
                if pipe.pipe_type == "down" and not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.add_score()
            if self.pipe_timer <= 0:
                self.spawn_pipes()
                self.pipe_timer = random.randint(50, 100)  # Reset timer to a random value
            self.pipe_timer -= 1

    def spawn_pipes(self):
        screen_width = GameConfig.SCREEN_DIMENSION[0]
        gap_height = random.randint(150, 200)
        pipe_height = 600

        x_position = screen_width
        y_top = random.randint(-400, -200)
        y_bottom = y_top + gap_height + pipe_height

        self.pipes.add(Pipes(self.screen, x_position, y_top, "up"))
        self.pipes.add(Pipes(self.screen, x_position, y_bottom, "down"))
        print(f"Spawned pipes at ({x_position}, {y_top}) and ({x_position}, {y_bottom})")
        print(f"Current pipes in group: {self.pipes.sprites()}")

    def game_over(self):
        self.scroll_speed = 0
        self.game_manager.record_score(self.score)
        self.game_manager.set_level(Levels.SCOREBOARD)





