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

        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 40)

        self.title_text = UIText(
            100, 50, 
            "",
            self.font_big,
            color=(255, 255, 255)
        )

        self.stats_text = UIText(
            100, 150,
            "",
            self.font_small,
            color=(255, 255, 255),
            line_spacing=10
        )

        self.ui_manager.add(self.title_text)
        self.ui_manager.add(self.stats_text)
        self.set_info({})
        EventManager.subscribe("SET_END_SCENE_INFO", self.set_info)

    def set_info(self, info : dict):
        self.success = info.get("success", self.success)
        self.stats = info.get("stats", self.stats)

        title_str = "MISSION COMPLETE" if self.success else "MISSION FAILED"
        self.title_text.set_text(title_str)

        stats_str = (
            f"Controller : {self.stats.controller}\n"
            f"Flight Time : {self.stats.flight_time:.1f} s\n"
            f"Distance : {self.stats.distance:.1f} m\n"
            f"Collision Time : {self.stats.collision_time: .2f}\n"
            f"Energy Used : {self.stats.energy_used:.1f} %\n"
            f"Score : {self.stats.score}\n\n"
            "[R] Restart\n"
            "[M] Main Menu"
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