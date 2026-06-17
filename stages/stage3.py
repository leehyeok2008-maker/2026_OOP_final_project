from .stage import Stage
from entities import *
from controllers import ManualController ,PIDManualController
import pygame
from pygame import Vector2
from utils import reader
from config import DEFAULT_TILE_TYPE
import random

class Stage3(Stage):

    def __init__(self):
        drone = Drone((2.0, 2.0), reader.load_image_from_file("images/drone.jpg"), 1, position=pygame.Vector2(3, 3), collider_scale=(0.8, 0.4))
        cargo = Cargo((1.0, 1.0), reader.load_image_from_file("images/cargo.jpeg"), 1, position=pygame.Vector2(3, 1))
        tile_map = TileMap(
            grid=reader.load_grid_from_file("stages/map1.txt"),
            tile_size=1.0,
            tile_types=DEFAULT_TILE_TYPE  # tile_sprites_dict에서 tile_types로 매개변수 교체
        )
        goal = Goal((1.0, 1.0), reader.load_image_from_file("images/drone.jpg"), 1, position=pygame.Vector2(2, 3))
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

        import random

        # 강풍
        self.wind_force = Vector2(1, 0)

        # 10초마다 방향 변경
        self.wind_timer = 10.0

        self.wind_directions = [
            Vector2(1, 0),  # 오른쪽
            Vector2(-1, 0),  # 왼쪽
            Vector2(0, 1),  # 아래
            Vector2(0, -1)  # 위
        ]

        # 상태
        self.cargo_attached = False

        # 안내 문구 표시 시간
        self.message_timer = 5.0

            
    def update(self, dt):
        # 바람 방향 변경 타이머
        self.wind_timer -= dt

        if self.wind_timer <= 0:
            self.wind_force = random.choice(
                self.wind_directions
            )

            self.wind_timer = 10.0

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

        # 목표 표시
        font = pygame.font.Font(None, 30)

        text = font.render(
            "GOAL",
            True,
            (0, 255, 0)
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
                "Stage 3 : 강풍 환경",
                "",
                "축하합니다! stage 2를 클리어하셨군요!",
                "하지만 아쉽게도 현실은 게임처럼 간단하지 않습니다.",
                "수많은 요소들이 상호작용하고, 언제나 예측할 수 없는 일들이 일어나죠.",
                "",
                "마침 바람이 불어오는군요.",
                "상하좌우. 바람은 당신이 상상하는 어떤 방향으로든 불어올 수 있습니다.",
                "과연 당신은 자연과 맞설 수 있을까요?",
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