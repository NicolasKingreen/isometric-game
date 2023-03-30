import pygame


class InputHandler:

    keys = {}  # should be initialized

    @staticmethod
    def update_keys():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                InputHandler.keys[event.key] = True
            elif event.type == pygame.KEYUP:
                InputHandler.keys[event.key] = False

