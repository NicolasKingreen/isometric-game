import pygame

import isogame.util
from isogame.asset_pool import AssetPool
from isogame.camera import Camera
from isogame.colors import *
from isogame.settings import *
from isogame.tilemap import TileMap, TileType, BuildingType, TILE_SIZE
from isogame.unit import Unit
from isogame.unit_command import UnitCommandMove


# TODO: chunk (8x8 tiles) system based batch rendering


class World:
    def __init__(self, size):
        self.size = size
        self.width, self.height = size  # in chunks

        self.tile_map = TileMap(size)
        self.camera = Camera((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        # self.camera = Camera((0, 0))
        self.selected_tile = None

        # self.units = [Unit((100, 100)), Unit((200, 300))]
        self.units = [Unit((100, 100))]

    def update(self, frame_time_s):
        self.camera.update(frame_time_s)

        for unit in self.units:
            unit.update(frame_time_s)

        mouse_pos = pygame.mouse.get_pos()
        x, y = self.get_grid_cell_from_screen_coordinates(*mouse_pos)
        if self.selected_tile != (x, y):
            self.selected_tile = x, y

        chunk_x, chunk_y = x // CHUNK_SIZE[0], y // CHUNK_SIZE[1]
        if pygame.mouse.get_pressed()[0] and self.within_bounds((x, y)):
            tile_x_local = x % CHUNK_SIZE[0]
            tile_y_local = y % CHUNK_SIZE[1]
            chunk = self.tile_map.chunks[chunk_x + chunk_y * self.width]
            chunk.tiles[tile_x_local + tile_y_local * CHUNK_SIZE[0]] = TileType.EMPTY
            chunk.prepare()
        elif pygame.mouse.get_pressed()[2] and self.within_bounds((x, y)):
            click_pos_inworld = self.screen_to_world_coordinates(*mouse_pos)
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # TODO: implement unit selection
                for unit in self.units:
                    unit.queue_command(UnitCommandMove(click_pos_inworld))
            else:
                for unit in self.units:
                    unit.set_command(UnitCommandMove(click_pos_inworld))

    def draw(self, surface: pygame.Surface):
        surface_rect = surface.get_rect()
        # print()
        for j, chunk in enumerate(self.tile_map.chunks):
            chunk_x = (j % self.width) * CHUNK_SIZE[0] * TILE_SIZE
            chunk_y = (j // self.width) * CHUNK_SIZE[1] * TILE_SIZE
            # print(f"Chunk {j}: {chunk_x, chunk_y}")
            chunk_x_iso, chunk_y_iso = isogame.util.cart_to_iso(chunk_x, chunk_y)
            chunk_x = (j % self.width) * CHUNK_SIZE[0] * TILE_SIZE + self.camera.position.x
            chunk_y = (j // self.width) * CHUNK_SIZE[1] * TILE_SIZE + self.camera.position.y
            # print(chunk_x_iso, chunk_y_iso)

            # TODO: add zoom dependence
            if surface_rect.colliderect((chunk_x_iso + self.camera.position.x,
                                         chunk_y_iso + self.camera.position.y,
                                         CHUNK_SIZE[0], CHUNK_SIZE[1])):  # if visible
                # for i, tile in enumerate(chunk.tiles):
                #     x = i % CHUNK_SIZE[0]
                #     y = i // CHUNK_SIZE[0]
                #
                #     # get 4 points per tile
                #     tile_points = TileMap.get_tile_points(x, y)
                #     # converting them from cartesian to isometric
                #     tile_points = [isogame.util.cart_to_iso(*point) for point in tile_points]
                #
                #     tile_points = isogame.util.apply_offset(tile_points, (chunk_x_iso, chunk_y_iso))
                #
                #     # applying camera offset
                #     tile_points = isogame.util.apply_offset(tile_points, self.camera.position)
                #
                #     # get top left corner of the 4-points polygon
                #     top_left = isogame.util.get_polygon_top_left_corner(tile_points)
                #     # decide which texture to lay down  # TODO: add system that resolves tile texture itself
                #     if tile == TileType.GRASS:
                #         image = AssetPool.get_image("tile_grass")
                #         surface.blit(image, top_left)
                #     elif tile == TileType.GRASS:
                #         image = AssetPool.get_image("tile_sand")
                #         surface.blit(image, top_left)
                #     elif tile == TileType.WATER:
                #         image = AssetPool.get_image("tile_water")
                #         surface.blit(image, top_left)
                #     elif tile == TileType.EMPTY:
                #         pass
                #
                #     # tile grid
                #     pygame.draw.polygon(surface, (63, 63, 63), tile_points, 1)
                #
                #     # buildings  # TODO: implement rotations
                #     # if self.tile_map.buildings[i] == BuildingType.HOUSE:
                #     #     new_x, new_y = top_left
                #     #     new_y -= TILE_SIZE
                #     #     image = AssetPool.get_image("building_house")
                #     #     surface.blit(image, (new_x+1, new_y))
                if not chunk.is_ready():  # loads chunk for the first time
                    chunk.prepare()

                surface.blit(chunk._surface, (chunk_x_iso + self.camera.position.x - CHUNK_SIZE[0] * TILE_SIZE,
                                              chunk_y_iso + self.camera.position.y))

        # selected tile
        if self.within_bounds(self.selected_tile):
            selected_tile_points = TileMap.get_tile_points(*self.selected_tile)
            selected_tile_points = [self.world_to_screen_coordinates(*point) for point in selected_tile_points]
            # pygame.draw.polygon(surface, (*FLAX, 127), selected_tile_points)
            pygame.draw.polygon(surface, FLAX, selected_tile_points, 3)

        for unit in self.units:
            unit_rect = unit.rect.copy()
            unit_rect.midbottom = self.world_to_screen_coordinates(*unit.position)

            # pygame.draw.rect(surface, (255, 0, 0), unit_rect, 1)
            isogame.util.draw_text(surface, f'{unit.current_command.__class__.__name__}', pygame.Vector2(unit_rect.midtop) - (35, 30))
            isogame.util.draw_text(surface, f'{tuple(round(d) for d in unit.position)}', pygame.Vector2(unit_rect.midtop) - (35, 15))
            surface.blit(unit.image, unit_rect)

        # pygame.draw.circle(surface, (255, 0, 0), self.camera.position, 3)

    def world_to_screen_coordinates(self, x, y):
        return pygame.Vector2(isogame.util.cart_to_iso(x, y)) + self.camera.position

    def screen_to_world_coordinates(self, x, y):

        # TODO: counter zoom... done, YAY!!!!
        camera_view = isogame.util.shrink_rect_by_factor((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), self.camera.zoom)

        x = x / SCREEN_WIDTH
        y = y / SCREEN_HEIGHT

        world_x = x * camera_view[2] + camera_view[0] - self.camera.position.x
        world_y = y * camera_view[3] + camera_view[1] - self.camera.position.y

        # removing camera offset
        # world_x = (x - self.camera.position.x) / self.camera.zoom
        # world_y = (y - self.camera.position.y) / self.camera.zoom

        # transforming isometric coordinates to cartesian
        cart_x, cart_y = isogame.util.iso_to_cart(world_x, world_y)

        return cart_x, cart_y

    def get_grid_cell_from_screen_coordinates(self, x, y):  # Where should it be?

        cart_x, cart_y = self.screen_to_world_coordinates(x, y)

        # transforming coordinates to grid position
        grid_x = cart_x // TILE_SIZE
        grid_y = cart_y // TILE_SIZE

        return int(grid_x), int(grid_y)

    def within_bounds(self, pos):
        x, y = pos
        if 0 <= x < self.width * CHUNK_SIZE[0]\
                and 0 <= y < self.height * CHUNK_SIZE[1]:
            return True
        return False
