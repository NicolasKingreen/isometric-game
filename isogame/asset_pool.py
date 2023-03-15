import pygame


IMAGES_PATH = "assets/graphics"
FONTS_PATH = "assets/fonts"


class AssetPool:
    images = {}
    fonts = {}

    @staticmethod
    def get_image(image_name):
        if AssetPool.images.get(image_name):
            return AssetPool.images[image_name]
        else:
            image = pygame.image.load(f"{IMAGES_PATH}/{image_name}.png").convert_alpha()
            AssetPool.images[image_name] = image
            return AssetPool.images[image_name]

    @staticmethod
    def get_font(font_name, size=32):
        font_name_sized = f"{font_name}_{size}"
        if AssetPool.fonts.get(font_name):
            return AssetPool.fonts[font_name_sized]
        else:
            font = pygame.font.Font(f"{FONTS_PATH}/{font_name}.ttf", size)
            AssetPool.fonts[font_name_sized] = font
            return AssetPool.fonts[font_name_sized]


def get_available_formats(file_name):
    # TODO: implement it later;
    # also would be great to have this class decide
    # which file format is preferred
    pass

