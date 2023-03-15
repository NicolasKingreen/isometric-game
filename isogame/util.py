import pygame

from isogame.asset_pool import AssetPool
from isogame.colors import *


def cart_to_iso(x, y):
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y


def iso_to_cart(x, y):
    cart_y = (2 * y - x) / 2
    cart_x = y + x
    return cart_x, cart_y


def get_polygon_top_left_corner(points):
    min_x = min(point[0] for point in points)
    min_y = min(point[1] for point in points)
    return min_x, min_y


def apply_offset(points, offset):
    x_offset, y_offset = offset
    points = [(x + x_offset, y + y_offset) for (x, y) in points]
    return points


def draw_text(surface, text, pos, color=BLACK, font_size=16):
    # TODO: optimize
    pygame.font.init()
    font = AssetPool.get_font("Ticketing", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=pos)
    surface.blit(text_surface, text_rect)


def scale_image(image, target_size):
    # size = image.get_size()
    # scale_factor = ()
    scaled_image = pygame.transform.scale(image, target_size)
    return scaled_image
