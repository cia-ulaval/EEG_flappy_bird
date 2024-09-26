from src.Bird import Bird
import pygame

class Game:
    def __init__(self, screen):
        self.init_variables(screen)
    
    def init_variables(self, screen):
        self.score = 0
        self.bird = Bird(screen)
        self.group = pygame.sprite.RenderPlain((self.bird))
    
    def click():
        pass
    
    def add_score():
        pass
    
    def draw(self, screen):
        self.group.draw(screen)
    
    def update(self):
        self.group.update()
    