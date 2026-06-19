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
        self.wind_force = Vector2(1.5, 0)

        # 약 10초마다 방향 변경
        self.wind_timer = 10.0

        self.wind_options = [
            {"force": Vector2(1.5, 0), "dir_text": "→"},
            {"force": Vector2(-1.5, 0), "dir_text": "←"},
            {"force": Vector2(0, 1.5), "dir_text": "↑"},
            {"force": Vector2(0, -1.5), "dir_text": "↑"}
        ]

        self.wind_dir_text = self.wind_options[0]["dir_text"]
        self.wind_panel = pygame.Surface((180, 45), pygame.SRCALPHA)
        self.wind_panel.fill((0, 0, 0, 160))
        
        self.ui_font = pygame.font.SysFont("malgungothic", 22)
        self.ui_font.set_bold(True)

    def update(self, dt):
        self.wind_timer -= dt
        if self.wind_timer <= 0:
            wind_option = random.choice(self.wind_options)
            self.wind_force = wind_option["force"] * random.uniform(0.5, 2.0)
            self.wind_dir_text = wind_option["dir_text"]
            self.wind_timer = random.uniform(5.0, 15.0)

        # 강풍 적용
        self.drone.rigidbody.apply_force(self.wind_force)
        if self.cargo: self.cargo.rigidbody.apply_force(self.wind_force)
        super().update(dt)

    def render(self, screen):
        # 부모의 맵, 기체, 목적지 등 렌더링
        super().render(screen)

        screen.blit(self.wind_panel, (screen.get_width() - 200, 20))
        
        text_surface = self.ui_font.render(f"강풍: {self.wind_force.length():.1f} N ({self.wind_dir_text})", True, (255, 69, 0))
        screen.blit(text_surface, (screen.get_width() - 190, 27))