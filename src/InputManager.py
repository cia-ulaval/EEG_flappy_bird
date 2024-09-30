import pygame

class InputManager:
    jump_down = False



    @staticmethod
    def handle_event(event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                InputManager.jump_down = True

    @staticmethod
    def refresh_inputs():
        InputManager.jump_down = False

    @staticmethod
    def is_jump_down():
        return InputManager.jump_down
