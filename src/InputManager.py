import pygame

class InputManager:
    jump_down = False
    echap_pressed = False


    @staticmethod
    def handle_event(event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                InputManager.jump_down = True
            if event.key == pygame.K_ESCAPE:
                InputManager.echap_pressed = True

    @staticmethod
    def refresh_inputs():
        InputManager.jump_down = False
        InputManager.echap_pressed = False

    @staticmethod
    def is_jump_down():
        return InputManager.jump_down
