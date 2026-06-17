import pygame
from config import *
from .scene import Scene
from data.stats import FlightStats
from pygame import Vector2
from stages import Stage, GenericStage
from managers import UIManager, EventManager
from ui import UIText


class GameScene(Scene):

    def __init__(self):
        
        self.stages : list[Stage] = [
            GenericStage(
                map_path="maps/map_tutorial1.txt",
                drone_pos=Vector2(12, 3),
                cargo_pos=Vector2(0, 0),
                goal_pos=Vector2(12, 3),
                has_cargo=False,
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 1)
            ),
            GenericStage(
                map_path="maps/map_tutorial2.txt",
                drone_pos=Vector2(4, 4),
                cargo_pos=Vector2(0, 0),
                goal_pos=Vector2(4, 4),
                has_cargo=False,
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 2)
            ),
            GenericStage(
                map_path="maps/map_tutorial3.txt",
                drone_pos=Vector2(12, 4),
                cargo_pos=Vector2(12, 3),
                goal_pos=Vector2(12, 10),
                goal_condition="CARGO_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 3)
            ),
        ]

        self.start_delay : list[float] = [
            2.0,
            2.0,
            2.0
        ]

        self.start_messages : list[str] = [
            "W키를 눌러 상승",
            "A/S를 눌러 좌우 회전",
            "R키를 눌러 화물 집기",
        ]

        #region UI 구성
        self.ui_manager = UIManager()

        title_font = pygame.font.SysFont("malgungothic", 100)
        title_font.set_bold(True)
        button_font = pygame.font.SysFont("malgungothic", 50)
        info_font = pygame.font.SysFont("malgungothic", 30)

        self.start_message_text = UIText(0, 0, self.start_messages[0], title_font, (255, 255, 255))
        self.start_message_text.center = (WIDTH//2, HEIGHT//2)
        self.ui_manager.add(self.start_message_text)
        #endregion
        
        self.total_time = 0.0
        self.total_distance = 0.0
        self.total_collision_time = 0.0
        self.total_energy_used = 0.0

        self.ui_timer = self.start_delay[0]

        self.current_stage_idx = 0
        self.current_stage = self.stages[0]
        EventManager.subscribe("CHANGE_STAGE", self.change_stage)
        EventManager.subscribe("FAIL_STAGE", self.fail_stage)
        EventManager.subscribe("COLLECT_INFO", self.collect_info)

    def change_stage(self, stage_num : int):
        self.current_stage_idx = stage_num 
        if self.current_stage_idx >= len(self.stages):
            EventManager.publish("CHANGE_SCENE", "END_SCENE")
            self._publish_end_scene_info(True)
        else:
            self.current_stage = self.stages[self.current_stage_idx]
            self.ui_timer = self.start_delay[self.current_stage_idx]
            self.start_message_text.set_text(self.start_messages[self.current_stage_idx])
            self.start_message_text.center = (WIDTH//2, HEIGHT//2)

    def fail_stage(self, *args):
        EventManager.publish("CHANGE_SCENE", "END_SCENE")
        self._publish_end_scene_info(False)

    def _publish_end_scene_info(self, status):
        EventManager.publish("SET_END_SCENE_INFO", {
            "success" : status,
            "stats" : FlightStats(
                controller = "나중에 추가",
                flight_time = self.total_time, 
                distance = self.total_distance, 
                collision_time = self.total_collision_time, 
                energy_used = self.total_energy_used, 
                score = self._calculate_score(),
            )
        })

    def collect_info(self, data : dict):
        ''' 
        displacement : float
        collision_time : float
        energy_used : float
        '''
        self.total_distance += data.get("displacement", 0.0)
        self.total_collision_time += data.get("collision_time", 0.0)
        self.total_energy_used += data.get("energy_used", 0.0)

    def _calculate_score(self) -> int:
        return round((1.1 ** self.total_collision_time) * self.total_time * self.total_distance * self.total_energy_used)

    def update(self, dt):
        if self.ui_timer > 0:
            self.ui_timer -= dt
            if self.ui_timer <= 0:
                self.start_message_text.set_text("")
        else:       
            self.total_time += dt
            self.current_stage.update(dt)
        self.ui_manager.update(dt)

    def render(self, screen):
        self.current_stage.render(screen)
        if self.ui_timer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128)) 
            screen.blit(overlay, (0, 0))
        self.ui_manager.render(screen)

    def __del__(self):
        '''EventManager로 인한 메모리 누수 방지'''
        try:
            EventManager.unsubscribe("CHANGE_STAGE", self.change_stage)
            EventManager.unsubscribe("FAIL_STAGE", self.fail_stage)
            EventManager.unsubscribe("COLLECT_INFO", self.collect_info)
        except (ValueError, AttributeError):
            pass