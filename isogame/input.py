import pygame


class InputHandler:

    keydowns = {}
    keyups = {}

    @staticmethod
    def get_input():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                InputHandler.keydowns[event.key] = True
                InputHandler.keyups[event.key] = False
            elif event.type == pygame.KEYUP:
                InputHandler.keyups[event.key] = True
                InputHandler.keydowns[event.key] = False

