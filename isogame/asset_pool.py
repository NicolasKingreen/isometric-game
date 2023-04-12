import pygame


IMAGES_PATH = "assets/graphics"
FONTS_PATH = "assets/fonts"


class AssetPool:
    _images = {}
    _fonts = {}

    @staticmethod
    def get_image(image_name) -> pygame.Surface:
        if AssetPool._images.get(image_name):
            return AssetPool._images[image_name]
        else:
            image = pygame.image.load(f"{IMAGES_PATH}/{image_name}.png").convert_alpha()
            AssetPool._images[image_name] = image
            return AssetPool._images[image_name]

    @staticmethod
    def add_image(image_name, image):
        if not AssetPool._images.get(image_name):
            AssetPool._images[image_name] = image
        else:
            print(f" ** Texture {image_name} exists")

    @staticmethod
    def get_font(font_name, size=32):
        font_name_sized = f"{font_name}_{size}"
        if AssetPool._fonts.get(font_name):
            return AssetPool._fonts[font_name_sized]
        else:
            font = pygame.font.Font(f"{FONTS_PATH}/{font_name}.ttf", size)
            AssetPool._fonts[font_name_sized] = font
            return AssetPool._fonts[font_name_sized]


def get_available_formats(file_name):
    # TODO: implement it later;
    # also would be great to have this class decide
    # which file format is preferred
    pass

