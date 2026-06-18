import pygame
from ui import UIText
from .scene import Scene
from data.stats import FlightStats
from managers import UIManager, InputManager, EventManager

class EndScene(Scene):

    def __init__(self):
        
        self.success = False
        self.stats = FlightStats()
        self.ui_manager = UIManager()

        big_font = pygame.font.SysFont("malgungothic", 72)
        info_font = pygame.font.SysFont("malgungothic", 40)

        self.title_text = UIText(
            100, 50, 
            "",
            big_font,
            color=(255, 255, 255)
        )

        self.stats_text = UIText(
            100, 180,
            "",
            info_font,
            color=(255, 255, 255),
            line_spacing=10
        )

        self.ui_manager.add(self.title_text)
        self.ui_manager.add(self.stats_text)
        self.set_info({})
        EventManager.subscribe("SET_END_SCENE_INFO", self.set_info)

    def set_info(self, info : dict):
        self.success = info.get("success", self.success)
        self.ending_type = info.get("type", "일반")
        self.stats = info.get("stats", self.stats)

        title_str = "미션 성공!" if self.success else "미션 실패..."
        self.title_text.set_text(title_str)

        stats_str = (
            f"종류 : {self.ending_type}\n"
            f"비행 시간 : {self.stats.flight_time:.1f} s\n"
            f"이동 거리 : {self.stats.distance:.1f} m\n"
            f"충돌 시간 : {self.stats.collision_time: .2f}s\n"
            f"에너지 사용 : {self.stats.energy_used:.1f} J\n"
            f"점수 : {self.stats.score}\n\n"
            "[R] 재시작 \n"
            "[M] 메인 메뉴"
        )
        self.stats_text.set_text(stats_str)

    def update(self, dt):
        # R : 재시작
        if InputManager.is_key_pressed(pygame.K_r):
            EventManager.publish("CHANGE_SCENE", "GAME_SCENE")
            
        # M : 메인메뉴
        elif InputManager.is_key_pressed(pygame.K_m):
            EventManager.publish("CHANGE_SCENE", "START_SCENE")

        self.ui_manager.update(dt)

    def render(self, screen):
        screen.fill((30, 30, 30))
        self.ui_manager.render(screen)