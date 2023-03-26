import pygame


from isogame.asset_pool import AssetPool
from isogame.colors import *


def cart_to_iso(x, y):
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y


def iso_to_cart(x, y):
    cart_x = x/2 + y
    cart_y = y - x/2
    return cart_x, cart_y


def islist(var):
    return type(var) in (int, type)


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


def scale_image_to_size(image, target_size):
    # size = image.get_size()
    # scale_factor = ()
    scaled_image = pygame.transform.scale(image, target_size)
    return scaled_image


def scale_image_by_factor(image: pygame.Surface, scale_factor):
    """
    scale factor could be 2d tuple
    """
    image_size = image.get_size()
    new_image_size = [d * scale_factor for d in image_size]
    return scale_image_to_size(image, new_image_size)


def scale_image_by_xy(image: pygame.Surface, xy_factors):
    """
    scales given image by x and y,
    therefore xy_factors should be 2d list/tuple
    """
    image_size = image.get_size()
    if len(xy_factors) == 2:
        new_image_size = [d * sf for d, sf in zip(image_size, xy_factors)]
        return new_image_size
    else:
        raise Exception("Scaling factors is incorrect (should be 2d list/tuple)")


if __name__ == '__main__':
    # tests
    test_image = pygame.Surface((32, 32))
    print(test_image)
    scaled_test_image = scale_image_by_factor(test_image, 2)
    print(scaled_test_image)
