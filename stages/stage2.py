from .stage import Stage
from entities import *
from controllers import ManualController ,PIDManualController
import pygame
from pygame import Vector2
from utils import reader
from config import DEFAULT_TILE_TYPE


class Stage2(Stage):

    def __init__(self):
        drone = Drone((2.0, 2.0), pygame.image.load("images/drone.jpg"), 1, position=pygame.Vector2(3, 3), collider_scale=(0.8, 0.4))
        cargo = Cargo((1.0, 1.0), pygame.image.load("images/cargo.jpeg"), 1, position=pygame.Vector2(3, 1))
        tile_map = TileMap(
            grid=reader.load_grid_from_file("stages/map1.txt"),
            tile_size=1.0,
            tile_types=DEFAULT_TILE_TYPE  # tile_sprites_dict에서 tile_types로 매개변수 교체
        )
        goal = Goal((1.0, 1.0), pygame.image.load("images/drone.jpg"), 2, position=pygame.Vector2(2, 3))
        super().__init__(
            drone=drone,
            cargo=cargo,
            tile_map=tile_map,
            controller=ManualController(drone),
            goal=goal,
        )

        # 목표지점
        self.goal_pos = Vector2(800, 300)
        self.goal_radius = 30

        # 강풍
        self.wind_force = Vector2(1, 0)

        # 상태
        self.cargo_attached = False

        # 안내 문구 표시 시간
        self.message_timer = 5.0

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # E키로 화물 연결
            if event.key == pygame.K_e:

                distance = (
                    self.drone.rigidbody.transform.position
                    -
                    self.cargo.rigidbody.transform.position
                ).length()

                if distance < 50:

                    self.cargo_attached = True

    def update(self, dt):

        # 강풍 적용
        self.drone.rigidbody.apply_force(
            self.wind_force
        )

        super().update(dt)

        # 안내문 타이머
        if self.message_timer > 0:
            self.message_timer -= dt

        # 성공 판정
        if (
            self.cargo.rigidbody.transform.position
            - self.goal_pos
        ).length() <= self.goal_radius:

            return "CLEAR"

        return None

    def render(self, screen):
        
        super().render(screen)
        
        # 목표 지점
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            self.goal_pos,
            self.goal_radius,
            2
        )

       
        screen.blit(
            text,
            (
                self.goal_pos.x - 20,
                self.goal_pos.y - 50
            )
        )

        # 튜토리얼 문구
        if self.message_timer > 0:

            tutorial = [
                "Stage 2 : 강풍 환경",
                "",
                "강풍이 불고 있습니다.",
                "드론이 계속 오른쪽으로 밀려납니다.",
                "",
                "화물 위로 이동하세요.",
                "E 키를 눌러 화물을 부착하세요.",
                "",
                "화물을 녹색 지점으로 운반하세요."
            ]

            y = 50

            for line in tutorial:

                text = font.render(
                    line,
                    True,
                    (255, 255, 255)
                )

                screen.blit(text, (50, y))

                y += 35

        # 상태 UI
        info = font.render(
            f"Wind : {self.wind_force.x:.0f} N ->",
            True,
            (255, 255, 255)
        )

        screen.blit(info, (20, 20))

        cargo_text = font.render(
            f"Cargo : {'Attached' if self.cargo_attached else 'Detached'}",
            True,
            (255, 255, 255)
        )

        screen.blit(cargo_text, (20, 55))