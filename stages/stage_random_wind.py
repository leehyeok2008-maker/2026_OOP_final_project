import pygame
from pygame import Vector2
from typing import Callable
import random
from .generic_stage import GenericStage

class StageRandomWind(GenericStage):

    def __init__(
        self, 
        map_path: str, 
        drone_pos: Vector2, 
        cargo_pos: Vector2, 
        goal_pos: Vector2, 
        goal_condition: str = "CARGO_ONLY", 
        has_cargo: bool = True, 
        goal_event: Callable[[], None] = lambda: None
    ):
        super().__init__(
            map_path=map_path,
            drone_pos=drone_pos,
            cargo_pos=cargo_pos,
            goal_pos=goal_pos,
            goal_condition=goal_condition,
            has_cargo=has_cargo,
            goal_event=goal_event
        )

        # 강풍
        self.wind_force = Vector2(1, 0)

        # 10초마다 방향 변경
        self.wind_timer = 10.0 

        self.wind_directions = [
            Vector2(1.5, 0),   # 오른쪽
            Vector2(-1.5, 0),  # 왼쪽
            Vector2(0, 1.5),   # 아래
            Vector2(0, -1.5)   # 위
        ]

    def update(self, dt):
        # 💡 바람 방향 변경 타이머 계산
        self.wind_timer -= dt
        if self.wind_timer <= 0:
            self.wind_force = random.choice(self.wind_directions)
            self.wind_timer = 10.0

        # 강풍 적용
        self.drone.rigidbody.apply_force(
            self.wind_force
        )

        super().update(dt)

    def render(self, screen):
        # 부모의 맵, 기체, 목적지 등 렌더링
        super().render(screen)