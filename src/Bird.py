import pygame
from src.util import load_image

from src.GameConfig import GameConfig


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.init_variables(screen)
        self.velocity = pygame.Vector2(0, 0)
    
    def init_variables(self, screen:pygame.Surface):
        self.const_image, self.const_rect = load_image("assets/brainDefault.png", -1)
        self.const_flap_image, self.const_flap_rect = load_image("assets/brainFlap.png", -1)
        self.const_mid_flap_image, self.const_mid_flap_rect = load_image("assets/brainMidFlap.png", -1)
        self.const_rect.center = (screen.get_width()/2,
                                  screen.get_height()/2)
        self.image = self.const_image
        self.rect = self.const_rect

        self.jump_timer = 0

    def rotate_around_center(self, image, angle, x,y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=(x,y)).center)
        return rotated_image, new_rect
    
    def update(self, dt):
        
        # position update
        self.gravity(dt)
        self.const_rect.center += self.velocity * dt

        # limit the character to the screen limit
        if self.const_rect.centery > GameConfig.SCREEN_DIMENSION.y - 20:
            self.const_rect.centery = GameConfig.SCREEN_DIMENSION.y - 20
            self.velocity.y = 0

        # change back to default sprite if finished jump
        if pygame.time.get_ticks() > self.jump_timer:
            self.image = self.const_mid_flap_image
        if pygame.time.get_ticks() > self.jump_timer + 30:
            self.image = self.const_image

        # rotation update, if not crashed on the ground
        # if self.const_rect.centery < GameConfig.SCREEN_DIMENSION.y:
        #     speed = 0.1
        #     angle = pygame.time.get_ticks() * speed
        #     self.image, self.rect = self.rotate_around_center(
        #         self.const_image,
        #         angle,
        #         self.const_rect.centerx,
        #         self.const_rect.centery 
        #     )

    def jump(self, dt):
        #changing frame for flap
        self.image = self.const_flap_image
        self.jump_timer = pygame.time.get_ticks() + 75

        jump_force = 300
        self.velocity.y = -jump_force

    def gravity(self, dt):
        gravity_force = 800
        self.velocity.y += gravity_force * dt

    def crashed(self):
        crashed = False
        if self.const_rect.centery == GameConfig.SCREEN_DIMENSION.y - 20:
            crashed = True
        return crashed

