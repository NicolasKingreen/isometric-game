import pygame
from pygame import Vector2

from isogame.settings import SCREEN_WIDTH, SCREEN_HEIGHT, EDGE_SCROLLING_PERCENT


class Camera:
    def __init__(self, start_pos=(0, 0)):
        self.position = Vector2(start_pos)
        self.move_direction = Vector2()
        self.move_vector = Vector2()
        self.speed = 500  # px/s

    def update(self, frame_time_s):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pressed_keys = pygame.key.get_pressed()

        # x
        if mouse_x > SCREEN_WIDTH * (1 - EDGE_SCROLLING_PERCENT)\
                or pressed_keys[pygame.K_d]:
            self.move_direction.x = -1
        elif mouse_x < SCREEN_WIDTH * EDGE_SCROLLING_PERCENT\
                or pressed_keys[pygame.K_a]:
            self.move_direction.x = 1
        else:
            self.move_direction.x = 0

        # y
        if mouse_y > SCREEN_HEIGHT * (1 - EDGE_SCROLLING_PERCENT)\
                or pressed_keys[pygame.K_s]:
            self.move_direction.y = -1
        elif mouse_y < SCREEN_HEIGHT * EDGE_SCROLLING_PERCENT\
                or pressed_keys[pygame.K_w]:
            self.move_direction.y = 1
        else:
            self.move_direction.y = 0

        self.move_vector and self.move_vector.normalize_ip()
        self.position += self.move_direction * self.speed * frame_time_s

