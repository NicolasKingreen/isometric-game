import pygame

import psutil
import os

import isogame.util
from isogame.colors import *
from isogame.hud import HUD
from isogame.input import InputHandler
from isogame.settings import *
from isogame.util import draw_text
from isogame.world import World


class Application:
    def __init__(self):
        pygame.display.set_caption("Isometric Game")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        self.draw_surface = pygame.Surface(SCREEN_SIZE)

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
            # self._get_input()
            self._update_states()
            self._render_graphics()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

                # elif event.key == pygame.K_e:
                #     self.world.camera.zoom *= 2
                # elif event.key == pygame.K_q:
                #     self.world.camera.zoom /= 2
            elif event.type == pygame.MOUSEWHEEL:
                # add_value = abs(event.y) ** 1 / self.world.camera.zoom
                # add_value = add_value if event.y > 0 else -add_value
                # self.world.camera.zoom += add_value

                # mouse_v = pygame.Vector2(pygame.mouse.get_pos())
                # camera_onscreen_v = self.world.world_to_screen_coordinates(*self.world.camera.position)
                # print(mouse_v, camera_onscreen_v)

                # self.dv = mouse_v - (self.world.camera.position + (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                # target_position = self.world.screen_to_world_coordinates(*mouse_v)

                self.world.camera.process_mouse_wheel(event.y)

    def _get_input(self):
        InputHandler.get_input()

    def _update_states(self):
        self.world.update(self.frame_time_s)

    def _render_graphics(self):
        self.draw_surface.fill((255, 255, 255))

        # game world
        self.world.draw(self.draw_surface)

        area_to_take = isogame.util.shrink_rect_by_factor(self.display_surface.get_rect(), self.world.camera.zoom)
        temp_surface = pygame.Surface(area_to_take[2:])
        temp_surface.blit(self.draw_surface, (0, 0), area_to_take)
        temp_surface = isogame.util.scale_image_by_factor(temp_surface, self.world.camera.zoom)
        self.display_surface.blit(temp_surface, (0, 0))

        # if self.world.camera.should_resize:
        #     draw_surface_tmp = isogame.util.scale_image_by_factor(self.draw_surface, self.world.camera.zoom)
        #     self.world.camera.should_resize = False
        #     self.display_surface.blit(draw_surface_tmp, (0, 0))
        # else:
        #     self.display_surface.blit(self.draw_surface, (0, 0))

        # ui  # TODO: ui takes a lot of resources, fix it
        # self.hud.draw(self.display_surface)
        draw_text(self.display_surface, f"{round(self.clock.get_fps())} fps ({self.cpu_usage}%/{int(self.mem_usage)}MB)", (3, 3 + TOP_BAR_HEIGHT))
        draw_text(self.display_surface, f"{self.world.get_grid_cell_from_screen_coordinates(*pygame.mouse.get_pos())}", (3, 3 + TOP_BAR_HEIGHT + 3 + 16))
        draw_text(self.display_surface, f"{self.world.camera.position}", (3, 3 + TOP_BAR_HEIGHT + 3 + 16 + 3 + 16))
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.display_surface, f"SCREEN: {mouse_pos}", (mouse_pos[0] + 15, mouse_pos[1]))
        draw_text(self.display_surface,
                  f"WORLD: {tuple(round(d) for d in self.world.screen_to_world_coordinates(*mouse_pos))}",
                  (mouse_pos[0] + 15, mouse_pos[1] + 15))
        draw_text(self.display_surface, f"ZOOM: {self.world.camera.zoom}x", (mouse_pos[0] + 15, mouse_pos[1] + 30))
        # if hasattr(self, 'dv'):
            # print(self.dv)
            # pygame.draw.circle(self.display_surface, (255, 255, 0), self.world.camera.position, 2)
            # pygame.draw.line(self.display_surface, (255, 255, 0), self.world.camera.position, -self.dv + (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 2)
            # pygame.draw.circle(self.display_surface, (255, 255, 0), -self.dv, 5)
        pygame.draw.circle(self.display_surface, (255, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 3)

        pygame.display.update()

    def stop(self):
        self.is_running = False
