import pygame
from src.util import load_image, rotate_around_center

from src.GameConfig import GameConfig


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.const_image, self.const_rect = load_image("assets/brainDefault.png", -1)
        self.const_flap_image, self.const_flap_rect = load_image("assets/brainFlap.png", -1)
        self.const_mid_flap_image, self.const_mid_flap_rect = load_image("assets/brainMidFlap.png", -1)
        self.const_rect.center = (screen.get_width() / 2,
                                  screen.get_height() / 2)
        self.image = self.const_image
        self.rect = self.const_rect
        self.first_jump = True

        self.jump_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.JUMP_FORCE = 800
        self.SPEED_BIRD_TILT = 40

    def update(self, dt):
        self.gravity(dt)
        self.const_rect.center += self.velocity * dt

        # limit the bird to the screen limit
        if self.const_rect.centery > GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE / 2.5:
            self.const_rect.centery = GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE / 2.5
            self.velocity.y = 0

        # change back to default sprite if finished jump
        next_image = self.const_flap_image
        if pygame.time.get_ticks() > self.jump_timer:
            next_image = self.const_mid_flap_image
        if pygame.time.get_ticks() > self.jump_timer + GameConfig.FLAP_ANIMATION_TIMING / 2:
            next_image = self.const_image

        # rotates the bird according to the velocity
        if self.const_rect.centery < GameConfig.SCREEN_DIMENSION.y:
            angle = max(-(self.velocity.y / self.JUMP_FORCE * self.SPEED_BIRD_TILT) + 45, -180)
        else:
            angle = 0
        if not self.first_jump:
            self.image, self.rect = rotate_around_center(
                next_image,
                angle,
                self.const_rect.centerx,
                self.const_rect.centery)

    def jump(self, dt):
        if self.first_jump:
            self.first_jump = False
        self.jump_timer = pygame.time.get_ticks() + GameConfig.FLAP_ANIMATION_TIMING

        # velocity change for jump
        self.velocity.y = -self.JUMP_FORCE

    def gravity(self, dt):
        if not self.first_jump:
            self.velocity.y += GameConfig.GRAVITY_FORCE * dt

    def crashed(self):
        crashed = False
        if self.const_rect.centery == GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE / 2.5:
            crashed = True
        return crashed
