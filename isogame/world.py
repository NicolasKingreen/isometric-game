import pygame

import isogame.util
from isogame.asset_pool import AssetPool
from isogame.camera import Camera
from isogame.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from isogame.tilemap import TileMap, TileType, TILE_SIZE


WORLD_SIZE = 40, 30
WORLD_WIDTH, WORLD_HEIGHT = WORLD_SIZE


# TODO: chunk system based batch rendering


class World:
    def __init__(self):
        self.tile_map = TileMap(WORLD_SIZE)
        # self.tile_map_surface = pygame.Surface((WORLD_WIDTH * TILE_SIZE * 2, WORLD_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        self.camera = Camera()

    def update(self, frame_time_s):
        self.camera.update(frame_time_s)

    def draw(self, surface):
        for i, tile in enumerate(self.tile_map.tiles):
            x = i % self.tile_map.width
            y = i // self.tile_map.width

            tile_points = TileMap.get_tile_points(x, y)
            tile_points = isogame.util.apply_offset(tile_points, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            tile_points = isogame.util.apply_offset(tile_points, self.camera.position)

            # tile texture
            top_left = isogame.util.get_polygon_top_left_corner(tile_points)

            if tile == TileType.GRASS:
                image = AssetPool.get_image("tile_grass")
            elif tile == TileType.EMPTY:
                image = pygame.Surface((64, 32), pygame.SRCALPHA)
            surface.blit(image, top_left)

            # tile grid
            pygame.draw.polygon(surface, (63, 63, 63),
                                tile_points, 1)

    def get_grid_cell_from_screen_coordinates(self, x, y):
        # TODO: fixxxx
        grid_x = x - self.camera.position.x - SCREEN_WIDTH // 2
        grid_y = y - self.camera.position.y - SCREEN_HEIGHT // 4
        grid_x, grid_y = isogame.util.iso_to_cart(grid_x, grid_y)
        grid_x //= TILE_SIZE
        grid_y //= TILE_SIZE
        return grid_x, grid_y
