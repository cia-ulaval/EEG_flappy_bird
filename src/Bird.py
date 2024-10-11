import pygame
from src.util import load_image

from src.GameConfig import GameConfig


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.init_variables(screen)
        self.velocity = pygame.Vector2(0, 0)
        self.jump_force = 800
    
    def init_variables(self, screen:pygame.Surface):
        self.const_image, self.const_rect = load_image("assets/nath_head_only.png", -1)
        self.const_rect.center = (screen.get_width()/2,
                                  screen.get_height()/2)
        self.image =  self.const_image
        self.rect = self.const_rect

    def rotate_around_center(self, image, angle, x,y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=(x,y)).center)
        return rotated_image, new_rect
    
    def update(self, dt):
        
        # position update
        self.gravity(dt)
        self.const_rect.center += self.velocity * dt

        # limit the character to the screen limit
        if self.const_rect.centery > GameConfig.SCREEN_DIMENSION.y:
            self.const_rect.centery = GameConfig.SCREEN_DIMENSION.y
            self.velocity.y = 0

        # rotation update, if not crashed on the ground
        if self.const_rect.centery < GameConfig.SCREEN_DIMENSION.y:
            angle = max(-(self.velocity.y / self.jump_force * 60) - 45, -180)
        else:
            angle = 0

        self.image, self.rect = self.rotate_around_center(
            self.const_image,
            angle,
            self.const_rect.centerx,
            self.const_rect.centery)


    def jump(self, dt):

        self.velocity.y = -self.jump_force

    def gravity(self, dt):
        gravity_force = 3000
        self.velocity.y += gravity_force * dt

