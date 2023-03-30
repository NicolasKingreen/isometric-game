import pygame

import psutil
import os

import isogame.util
from isogame.colors import *
from isogame.hud import HUD
from isogame.input import InputHandler
from isogame.settings import *
from isogame.util import draw_text, cart_to_iso, iso_to_cart, apply_offset
from isogame.world import World


class Application:
    def __init__(self):
        pygame.display.set_caption("Isometric Game")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()
        self.frame_time_ms = 0
        self.frame_time_s = 0

        self.process = psutil.Process(os.getpid())
        self.process.cpu_percent()
        self.cpu_percent_interval = 1
        self.cpu_percent_timer = 0
        self.cpu_usage = 0
        self.mem_usage = 0

        # self.input_handler = InputHandler

        self.is_running = False

        self.world = World(WORLD_SIZE)
        self.hud = HUD()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.frame_time_ms = self.clock.tick(TARGET_FPS)
            self.frame_time_s = self.frame_time_ms / 1000.
            self.cpu_percent_timer += self.frame_time_s
            if self.cpu_percent_timer >= self.cpu_percent_interval:
                self.cpu_usage = self.process.cpu_percent()
                self.mem_usage = self.process.memory_info().rss / 1024 / 1024  # mb
                self.cpu_percent_timer = 0
            self._process_events()
            # InputHandler.update_keys()
            self._update_states()
            self._render_graphics()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

    def _update_states(self):
        self.world.update(self.frame_time_s)

    def _render_graphics(self):
        self.display_surface.fill((255, 255, 255))
        self.world.draw(self.display_surface)
        self.hud.draw(self.display_surface)
        draw_text(self.display_surface, f"{round(self.clock.get_fps())} fps ({self.cpu_usage}%/{int(self.mem_usage)}MB", (3, 3 + TOP_BAR_HEIGHT))
        draw_text(self.display_surface, f"{self.world.get_grid_cell_from_screen_coordinates(*pygame.mouse.get_pos())}", (3, 3 + TOP_BAR_HEIGHT + 3 + 16))
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.display_surface, f"{mouse_pos}", (mouse_pos[0] + 15, mouse_pos[1]))
        pygame.display.update()

    def stop(self):
        self.is_running = False
