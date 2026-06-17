import pygame
from data import *

WIDTH = 1200
HEIGHT = 900
FPS = 60
BACKGROUND_COLOR = (255, 255, 255)

APP_NAME = "Drone Delivery"
DEFAULT_PX_PER_METER = 48
DEFAULT_IMAGE = pygame.image.load("images/DEFAULT_IMAGE.png")
DEFAULT_TILE_TYPE = {
    1: TileType(
        name="ground",
        sprite_map={
            0: pygame.image.load("images/tile_images/row-4-column-4.png"),
            1: pygame.image.load("images/tile_images/row-3-column-4.png"),
            2: pygame.image.load("images/tile_images/row-1-column-4.png"),
            3: pygame.image.load("images/tile_images/row-2-column-4.png"),
            4: pygame.image.load("images/tile_images/row-4-column-3.png"),
            5: pygame.image.load("images/tile_images/row-3-column-3.png"),
            6: pygame.image.load("images/tile_images/row-1-column-3.png"),
            7: pygame.image.load("images/tile_images/row-2-column-3.png"),
            8: pygame.image.load("images/tile_images/row-4-column-1.png"),
            9: pygame.image.load("images/tile_images/row-3-column-1.png"),
            10: pygame.image.load("images/tile_images/row-1-column-1.png"),
            11: pygame.image.load("images/tile_images/row-2-column-1.png"),
            12: pygame.image.load("images/tile_images/row-4-column-2.png"),
            13: pygame.image.load("images/tile_images/row-3-column-2.png"),
            14: pygame.image.load("images/tile_images/row-1-column-2.png"),
            15: pygame.image.load("images/tile_images/row-2-column-2.png"),
        },
        is_solid=True,      # 물리 장벽 적용
        is_collidable=True  # 충돌 감지 등록
    )
}

