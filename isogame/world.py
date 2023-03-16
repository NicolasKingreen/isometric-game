import pygame

import isogame.util
from isogame.asset_pool import AssetPool
from isogame.camera import Camera
from isogame.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from isogame.tilemap import TileMap, TileType, TILE_SIZE


# TODO: chunk (8x8 tiles) system based batch rendering


class World:
    def __init__(self, size):
        self.size = size
        self.width, self.height = size

        self.tile_map = TileMap(size)
        self.camera = Camera((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    def update(self, frame_time_s):
        self.camera.update(frame_time_s)

        mouse_pos = pygame.mouse.get_pos()
        x, y = self.get_grid_cell_from_screen_coordinates(*mouse_pos)
        if pygame.mouse.get_pressed()[0] and self.within_bounds((x, y)):
            self.tile_map.tiles[int(x) + int(y) * self.width] = TileType.EMPTY

    def draw(self, surface):
        for i, tile in enumerate(self.tile_map.tiles):
            x = i % self.tile_map.width
            y = i // self.tile_map.width

            # get 4 points per tile
            tile_points = TileMap.get_tile_points(x, y)
            # converting them from cartesian to isometric
            tile_points = [isogame.util.cart_to_iso(*point) for point in tile_points]
            # applying camera offset
            tile_points = isogame.util.apply_offset(tile_points, self.camera.position)
            # get top left corner of the 4-points polygon
            top_left = isogame.util.get_polygon_top_left_corner(tile_points)
            # decide which texture to lay down  # TODO: add system that resolves tile texture itself
            if tile == TileType.GRASS:
                image = AssetPool.get_image("tile_grass")
                surface.blit(image, top_left)
            elif tile == TileType.GRASS:
                image = AssetPool.get_image("tile_sand")
                surface.blit(image, top_left)
            elif tile == TileType.WATER:
                image = AssetPool.get_image("tile_water")
                surface.blit(image, top_left)
            elif tile == TileType.EMPTY:
                pass

            # tile grid
            pygame.draw.polygon(surface, (63, 63, 63), tile_points, 1)

    def get_grid_cell_from_screen_coordinates(self, x, y):  # Where should it be?

        # removing camera offset
        world_x = x - self.camera.position.x
        world_y = y - self.camera.position.y

        # transforming isometric coordinates to cartesian
        cart_x, cart_y = isogame.util.iso_to_cart(world_x, world_y)

        # transforming coordinates to grid position
        grid_x = cart_x // TILE_SIZE
        grid_y = cart_y // TILE_SIZE

        return grid_x, grid_y

    def within_bounds(self, pos):
        x, y = pos
        if 0 <= x < self.width\
                and 0 <= y < self.height:
            return True
        return False
