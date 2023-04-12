import pygame
from pygame import Vector2

from isogame.input import InputHandler
from isogame.settings import SCREEN_WIDTH, SCREEN_HEIGHT, EDGE_SCROLLING_PERCENT
from isogame.util import lerp

MIN_ZOOM = 1
MAX_ZOOM = 8


class Camera:
    def __init__(self, start_pos=(0, 0)):
        self.position = Vector2(start_pos)
        self.move_direction = Vector2()
        self.move_vector = Vector2()
        self.speed = 1000  # px/s
        self.zoom = 2
        # self.should_resize = False

    def update(self, frame_time_s):

        # TODO: add middle mouse button grab

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pressed_keys = pygame.key.get_pressed()
        # pressed_keys = InputHandler.keys

        # x
        if mouse_x >= SCREEN_WIDTH * (1 - EDGE_SCROLLING_PERCENT) - 1 \
                or pressed_keys[pygame.K_d]:
            self.move_direction.x = -1
        elif mouse_x <= SCREEN_WIDTH * EDGE_SCROLLING_PERCENT\
                or pressed_keys[pygame.K_a]:
            self.move_direction.x = 1
        else:
            self.move_direction.x = 0

        # y
        if mouse_y >= SCREEN_HEIGHT * (1 - EDGE_SCROLLING_PERCENT) - 1 \
                or pressed_keys[pygame.K_s]:
            self.move_direction.y = -1
        elif mouse_y <= SCREEN_HEIGHT * EDGE_SCROLLING_PERCENT\
                or pressed_keys[pygame.K_w]:
            self.move_direction.y = 1
        else:
            self.move_direction.y = 0

        # zoom
        # if pressed_keys[pygame.K_e]:
        #     self.zoom *= 2
        #     # self.should_resize = True
        # elif pressed_keys[pygame.K_q]:
        #     self.zoom /= 2
        #     # self.should_resize = True

        self.move_vector and self.move_vector.normalize_ip()
        self.position += self.move_direction * self.speed / self.zoom * frame_time_s

    def process_mouse_wheel(self, dy):
        from math import copysign
        # TODO: make zoom towards mouse cursor

        old_zoom = self.zoom
        old_position = self.position.copy()

        # self.zoom += dy / 10  # step is 0.1
        # self.zoom += self.zoom / 5 * dy
        sign = copysign(1, dy)
        self.zoom += sign
        # self.zoom = round(self.zoom, 2)
        self.zoom = round(self.zoom)
        self.zoom = min(max(MIN_ZOOM, self.zoom), MAX_ZOOM)

        # zoom to cursor
        if self.zoom != old_zoom:
            screen_size = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
            screen_center = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            mouse_pos = Vector2(pygame.mouse.get_pos())

            # x1 and x2 work perfectly
            divisor = (1/2)**old_zoom if sign > 0 else (1/2)**self.zoom
            dv = sign * (screen_center - mouse_pos) * divisor
            self.position += dv

            # divider = 2**self.zoom if sign > 0 else 2**old_zoom
            # new_center = old_position - screen_center
            # divider = self.zoom if sign > 0 else old_zoom
            # new_position = new_center + sign * (screen_center - mouse_pos) / divider
            # self.position = new_position

