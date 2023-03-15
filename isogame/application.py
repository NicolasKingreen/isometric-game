import pygame

from isogame.colors import *
from isogame.hud import HUD
from isogame.settings import SCREEN_SIZE, TARGET_FPS, TOP_BAR_HEIGHT
from isogame.util import draw_text, cart_to_iso, iso_to_cart, apply_offset
from isogame.world import World


class Application:
    def __init__(self):
        pygame.display.set_caption("Isometric Game")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()
        self.frame_time_ms = 0
        self.frame_time_s = 0

        self.is_running = False

        self.world = World()
        self.hud = HUD()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.frame_time_ms = self.clock.tick(TARGET_FPS)
            self.frame_time_s = self.frame_time_ms / 1000.
            self._process_events()
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
        draw_text(self.display_surface, f"{round(self.clock.get_fps())} fps", (3, 3 + TOP_BAR_HEIGHT))
        draw_text(self.display_surface, f"{cart_to_iso(*self.world.get_grid_cell_from_screen_coordinates(*pygame.mouse.get_pos()))}", (3, 3 + TOP_BAR_HEIGHT + 3 + 16))
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.display_surface, f"{mouse_pos}", (mouse_pos[0] + 15, mouse_pos[1]))
        pygame.display.update()

    def stop(self):
        self.is_running = False
