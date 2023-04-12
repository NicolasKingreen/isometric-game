import pygame
import random
import noise

from enum import Enum, IntEnum


import isogame.util
from isogame.settings import *
from isogame.asset_pool import AssetPool


TILE_SIZE = 32


class TileType(IntEnum):
    EMPTY = 0
    GRASS = 1
    SAND = 2
    WATER = 3


class BuildingType(Enum):
    EMPTY = 0
    HOUSE = 1


class Tile:  # do I need it?
    def __init__(self, tile_type: TileType):
        self.type = tile_type


class Chunk:
    def __init__(self, tiles):
        self.tiles = tiles
        self._surface = None
        self._should_redraw = False

    def prepare(self):
        self._surface = self._render_tiles()

    def is_ready(self):
        return self._surface is not None

    def _render_tiles(self):
        surface = pygame.Surface((CHUNK_SIZE[0] * TILE_SIZE * 2, CHUNK_SIZE[1] * TILE_SIZE), pygame.SRCALPHA)
        for i, tile in enumerate(self.tiles):
            x = i % CHUNK_SIZE[0]
            y = i // CHUNK_SIZE[0]

            tile_points = TileMap.get_tile_points(x, y)
            tile_points = [isogame.util.cart_to_iso(*point) for point in tile_points]
            tile_points = isogame.util.apply_offset(tile_points, (CHUNK_SIZE[0] * TILE_SIZE, 0))
            top_left = isogame.util.get_polygon_top_left_corner(tile_points)
            if tile == TileType.GRASS:
                image = AssetPool.get_image("tile_grass")
                surface.blit(image, top_left)
            elif tile == TileType.SAND:
                image = AssetPool.get_image("tile_sand")
                surface.blit(image, top_left)
            elif tile == TileType.WATER:
                image = AssetPool.get_image("tile_water")
                surface.blit(image, top_left)
            elif tile == TileType.EMPTY:
                pass

            pygame.draw.polygon(surface, (63, 63, 63), tile_points, 1)

        return surface


class TileMap:
    def __init__(self, size):
        self.width, self.height = size

        self.chunks = [None] * (self.width * self.height)
        # self.tiles = [TileType.EMPTY] * (self.width * self.height)
        # self.buildings = [BuildingType.EMPTY] * (self.width * self.height)

        # some world generation logic
        for i, chunk in enumerate(self.chunks):
            tiles = [TileType.EMPTY] * (CHUNK_SIZE[0] * CHUNK_SIZE[1])
            for j, tile in enumerate(tiles):

                # tiles
                # r = random.randint(1, 100)
                # if r <= 10:
                #     tiles[j] = TileType.SAND
                tiles[j] = TileType.GRASS

                # buildings
                # r = random.randint(1, 100)
                # if r <= 3:
                #     self.buildings[i] = BuildingType.HOUSE
            self.chunks[i] = Chunk(tiles)

        self.generate_lakes()

    def generate_lakes(self):
        # got river...
        for i, chunk in enumerate(self.chunks):
            chunk_x = (i % WORLD_WIDTH)
            chunk_y = (i // WORLD_WIDTH)
            for j, tile in enumerate(chunk.tiles):
                tile_x_local = (j % CHUNK_SIZE[0])
                tile_y_local = (j // CHUNK_SIZE[0])

                tile_x_global = chunk_x * CHUNK_SIZE[0] + tile_x_local
                tile_y_global = chunk_y * CHUNK_SIZE[1] + tile_y_local

                world_width_tiles = self.width * CHUNK_SIZE[0]
                world_height_tiles = self.height * CHUNK_SIZE[1]

                noise_x = tile_x_global / world_width_tiles
                noise_y = tile_y_global / world_height_tiles
                tile_noise = noise.pnoise2(noise_x, noise_y)
                if abs(tile_noise) < 0.02:
                    chunk.tiles[tile_x_local + tile_y_local * CHUNK_SIZE[0]] = TileType.WATER
            chunk._surface = chunk._render_tiles()

    @staticmethod
    def get_tile_points(grid_x, grid_y):
        """Returns 4 cartesian points of a tile as a list"""
        points = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]
        return points


