import pygame
from src.util import load_image

from src.GameConfig import GameConfig


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.init_variables(screen)
        self.velocity = pygame.Vector2(0, 0)
        self.JUMP_FORCE = 800
        self.SPEED_BIRD_TILT = 40
    
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
        if self.const_rect.centery > GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE/2.5:
            self.const_rect.centery = GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE/2.5
            self.velocity.y = 0

        # change back to default sprite if finished jump
        next_image = self.const_flap_image
        if pygame.time.get_ticks() > self.jump_timer:
            next_image = self.const_mid_flap_image
        if pygame.time.get_ticks() > self.jump_timer + 50:
            next_image = self.const_image


        # rotates the bird according to the velocity
        if self.const_rect.centery < GameConfig.SCREEN_DIMENSION.y:
            angle = max(-(self.velocity.y/ self.JUMP_FORCE * self.SPEED_BIRD_TILT) + 45, -180)
        else:
            angle = 0
        self.image, self.rect = self.rotate_around_center(
            next_image,
            angle,
            self.const_rect.centerx,
            self.const_rect.centery)

    def jump(self, dt):
        # changing frame for flap
        self.jump_timer = pygame.time.get_ticks() + 95
        
        # velocity change for jump
        self.velocity.y = -self.JUMP_FORCE

    def gravity(self, dt):
        self.velocity.y += GameConfig.GRAVITY_FORCE * dt

    def crashed(self):
        crashed = False
        if self.const_rect.centery == GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE/2.5:
            crashed = True
        return crashed

