import pygame
from pygame import Vector2
from typing import Callable
from .generic_stage import GenericStage

class StageStaticWind(GenericStage):

    def __init__(
        self, 
        map_path: str, 
        drone_pos: Vector2, 
        cargo_pos: Vector2, 
        goal_pos: Vector2, 
        goal_condition : str = "CARGO_ONLY", 
        has_cargo : bool = True, 
        goal_event : Callable[[], None] = lambda: None
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
        self.wind_force = Vector2(1.5, 0.0) 
        
        self.wind_panel = pygame.Surface((180, 40), pygame.SRCALPHA)
        self.wind_panel.fill((0, 0, 0, 160))
        
        self.ui_font = pygame.font.SysFont("malgungothic", 22)
        self.ui_font.set_bold(True)

    def update(self, dt):
        # 강풍 적용
        self.drone.rigidbody.apply_force(self.wind_force)
        if self.cargo:
            self.cargo.rigidbody.apply_force(self.wind_force)
        
        super().update(dt)

    def render(self, screen):
        super().render(screen)
        
        screen.blit(self.wind_panel, (screen.get_width() - 200, 20))
        
        text_surface = self.ui_font.render(f"강풍: {self.wind_force.length():.1f} N (→)", True, (255, 69, 0))
        screen.blit(text_surface, (screen.get_width() - 190, 27))