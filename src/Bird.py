import pygame
import pygame.gfxdraw
from src import util

class Bird(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.init_variables(screen)
    
    def init_variables(self, screen:pygame.Surface):
        self.const_image, self.const_rect = util.load_image("nath_head_only.png", -1)
        self.const_rect.center = (screen.get_width()/2, screen.get_height()/2)
        self.image = self.const_image
        self.rect = self.const_rect
    
    def rotate_around_center(self, image, angle, x,y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center=(x,y)).center)
        return rotated_image, new_rect
    
    def update(self):
        speed = 0.1
        angle = pygame.time.get_ticks() * speed
        
        self.image, self.rect = self.rotate_around_center(
            self.const_image,
            angle,
            self.const_rect.centerx,
            self.const_rect.centery
        )
        
    def jump(self):
        pass

