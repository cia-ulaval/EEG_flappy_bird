import pygame
from src.util import load_image_rect, rotate_around_center
from src.GameConfig import GameConfig

class Bird(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.JUMP_FORCE = 800
        self.SPEED_BIRD_TILT = 40
        self.screen = screen
        self.jump_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.bird_image, self.bird = load_image_rect("assets/brainDefault.png", -1)
        self.bird_flap_image, self.bird_flap_rect = load_image_rect("assets/brainFlap.png", -1)
        self.bird_mid_flap_image, self.bird_mid_flap_rect = load_image_rect("assets/brainMidFlap.png", -1)
        self.bird.center = (screen.get_width() / 2,
                                  screen.get_height() / 2)
        self.first_jump = True
        self.image = self.bird_image
        self.rect = self.bird
        self.collision_rect = self.bird.inflate(-20, -20)

    def update(self, dt):
        self.gravity(dt)
        self.bird.center += self.velocity * dt
        self.collision_rect.center = self.rect.center

        if self.bird.centery > GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE / 2.5:
            self.bird.centery = GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE / 2.5
            self.velocity.y = 0

        next_image = self.bird_flap_image
        if pygame.time.get_ticks() > self.jump_timer:
            next_image = self.bird_mid_flap_image
        if pygame.time.get_ticks() > self.jump_timer + GameConfig.FLAP_ANIMATION_TIMING / 2:
            next_image = self.bird_image

        if self.bird.centery < GameConfig.SCREEN_DIMENSION.y:
            angle = max(-(self.velocity.y / self.JUMP_FORCE * self.SPEED_BIRD_TILT) + 45, -180)
        else:
            angle = 0
        if not self.first_jump:
            self.image, self.rect = rotate_around_center(
                next_image,
                angle,
                self.bird.centerx,
                self.bird.centery)

    def jump(self, dt):
        if self.first_jump:
            self.first_jump = False
        self.jump_timer = pygame.time.get_ticks() + GameConfig.FLAP_ANIMATION_TIMING

        self.velocity.y = -self.JUMP_FORCE

    def gravity(self, dt):
        if not self.first_jump:
            self.velocity.y += GameConfig.GRAVITY_FORCE * dt

    def crashed(self):
        crashed = False
        if self.bird.centery == GameConfig.SCREEN_DIMENSION.y - GameConfig.GROUND_SPACE / 2.5:
            crashed = True
        return crashed

    def reset_velocity(self):
        self.velocity.x = 0
        self.velocity.y = 0

    def reset_first_jump(self):
        self.first_jump = True