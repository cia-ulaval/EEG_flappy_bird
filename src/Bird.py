import pygame


class Bird:
    def __init__(self):
        self.init_variables()
    
    def init_variables(self):
        self.position = pygame.Vector2(0,0)
        self.velocity = pygame.Vector2(0,0)
        self.hitbox = pygame.Vector2(0,0)
        
    def jump(self):
        pass
    
    def draw(self):
        pass
