from .stage import Stage
from entities import *
from controllers import ManualController ,PIDManualController
import pygame
from utils import reader

class Stage1(Stage):

    def __init__(self):
        self.drone = Drone((2.0, 2.0), pygame.image.load("images/drone.jpg"), 1, position=pygame.Vector2(3, 3), collider_scale=(0.8, 0.4))
        self.cargo = Cargo((1.0, 1.0), pygame.image.load("images/cargo.jpeg"), 1, position=pygame.Vector2(5, 6))
        self.tile_map = TileMap(
            grid=reader.load_grid_from_file("stages/map1.txt"),
            tile_size=1.0,
            tile_sprites_dict={1: pygame.image.load("images/tile_images/row-1-column-2.png")}
        )
        super().__init__(
            drone=self.drone,
            cargo=self.cargo,
            map=self.tile_map,
            controller=PIDManualController(self.drone),
        )

        self.tutorial_step = 0
        self.font = pygame.font.Font(None, 40)

    def update(self, dt):

        super().update(dt)
        '''
        if self.tutorial_step == 0:

            if self.drone.position.y < 300:
                self.tutorial_step = 1

        elif self.tutorial_step == 1:

            if self.left_target_reached:
                self.tutorial_step = 2

        elif self.tutorial_step == 2:

            if self.cargo_attached:
                self.tutorial_step = 3

        elif self.tutorial_step == 3:

            if self.goal_reached:
                return "CLEAR"
        '''

    def get_tutorial_text(self):

        texts = [
            "W 키를 눌러 상승하세요.",
            "A, D 키로 이동하세요.",
            "화물 위로 이동하세요.",
            "화물을 목적지까지 운반하세요."
        ]

        return texts[self.tutorial_step]

    def render(self, screen):

        super().render(screen)

        text = self.font.render(
            self.get_tutorial_text(),
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 20))