import random

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
    WATER = 3


class Tile:  # do I need it?
    def __init__(self, tile_type: TileType):
        self.type = tile_type


class TileMap:
    def __init__(self, size):
        self.width, self.height = size

        self.tiles = [TileType.EMPTY] * (self.width * self.height)
        # some world generation logic
        for i, tile in enumerate(self.tiles):
            x = i % self.width
            y = i // self.width

            r = random.randint(1, 100)

            if r <= 10:
                self.tiles[i] = TileType.WATER
            elif r <= 20:
                self.tiles[i] = TileType.SAND
            else:
                self.tiles[i] = TileType.GRASS



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


