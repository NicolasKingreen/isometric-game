import pygame

from isogame.asset_pool import AssetPool
from isogame.colors import *
from isogame.settings import *
from isogame.util import draw_text, scale_image_to_size


class HUD:
    def __init__(self):

        # top bar
        self.top_bar_surface = pygame.Surface((SCREEN_WIDTH, TOP_BAR_HEIGHT), pygame.SRCALPHA)
        self.top_bar_surface.fill((*TAUPE_GRAY, 175))

        # bottom menu
        self.bottom_menu_surface = pygame.Surface((SCREEN_WIDTH, BOTTOM_MENU_HEIGHT), pygame.SRCALPHA)
        self.bottom_menu_surface.fill((*TAUPE_GRAY, 175))
        self.bottom_menu = HUDMenu()

    def draw(self, surface):
        surface.blit(self.top_bar_surface, (0, 0))
        draw_text(surface, "World Size: 40x30", (3, 4), PLATINUM, 24)
        draw_text(surface, "Some Dumb Text: good morning! :)", (250, 4), PLATINUM, 24)
        draw_text(surface, f"Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", (700, 4), PLATINUM, 24)
        draw_text(surface, "Version: 0.0.0pre-alpha01", (SCREEN_WIDTH - 280, 4), PLATINUM, 24)

        surface.blit(self.bottom_menu_surface, (0, SCREEN_HEIGHT - BOTTOM_MENU_HEIGHT))
        self.bottom_menu.draw(surface)


class HUDMenu:
    def __init__(self):
        self.items = []

        menu_item_01_image = scale_image_to_size(AssetPool.get_image("menu_item_01"), HUD_ITEM_IMAGE_SIZE)
        self.items.append(HUDItem(menu_item_01_image))

        menu_item_02_image = scale_image_to_size(AssetPool.get_image("menu_item_02"), HUD_ITEM_IMAGE_SIZE)
        self.items.append(HUDItem(menu_item_02_image))

        menu_item_03_image = pygame.Surface(HUD_ITEM_IMAGE_SIZE)
        menu_item_03_image.fill(MOSS_GREEN)
        self.items.append(HUDItem(menu_item_03_image))

        menu_item_04_image = pygame.Surface(HUD_ITEM_IMAGE_SIZE)
        menu_item_04_image.fill(FLAX)
        self.items.append(HUDItem(menu_item_04_image))

    def draw(self, surface):
        for i, item in enumerate(self.items):
            x = i // 2 * (HUD_ITEM_SIZE[0] + HUD_ITEM_MARGIN) + HUD_ITEM_MARGIN
            y = i % 2 * (HUD_ITEM_SIZE[1] + HUD_ITEM_MARGIN) + HUD_ITEM_MARGIN + (SCREEN_HEIGHT - BOTTOM_MENU_HEIGHT)
            surface.blit(item.image, (x, y))


class HUDItem:
    def __init__(self, image):
        bg_image = pygame.Surface(HUD_ITEM_SIZE)
        bg_image.fill(DIM_GRAY)
        bg_image.blit(image, HUD_ITEM_PADDING)
        self.image = bg_image

