import pygame

from enum import Enum


import isogame.util
from isogame.settings import *
from isogame.asset_pool import AssetPool


TILE_SIZE = 32


class TileType(Enum):
    EMPTY = 0
    GRASS = 1
    SAND = 2


class Tile:  # do I need it?
    def __init__(self, tile_type: TileType):
        self.type = tile_type


class TileMap:
    def __init__(self, size):
        self.width, self.height = size
        self.tiles = [TileType.GRASS] * (self.width * self.height)
        self.tiles[0] = TileType.EMPTY
        self.tiles[1] = TileType.EMPTY

    def draw(self, surface):  # I guess rendering should be in a different place...
        for i, tile in enumerate(self.tiles):
            x = i % self.width
            y = i // self.width

            tile_points = TileMap.get_tile_points(x, y)
            tile_points = isogame.util.apply_offset(tile_points, (SCREEN_WIDTH, SCREEN_HEIGHT))

            # tile texture
            top_left = isogame.util.get_polygon_top_left_corner(tile_points)
            image = AssetPool.get_image("tile_grass")
            surface.blit(image, top_left)

            # tile grid
            pygame.draw.polygon(surface, (63, 63, 63),
                                tile_points, 1)

    @staticmethod
    def get_tile_points(grid_x, grid_y, isometric=True):
        points = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]
        if isometric:
            points = [isogame.util.cart_to_iso(*point) for point in points]
        return points


