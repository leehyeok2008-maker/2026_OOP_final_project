import math
import pygame
from config import *
from .scene import Scene
from data.stats import FlightStats
from pygame import Vector2
from stages import *
from managers import UIManager, EventManager
from ui import *

class GameScene(Scene):

    def __init__(self):
        
        self.stages : list[Stage] = [
            GenericStage(
                map_path="maps/map_tutorial1.txt",
                drone_pos=Vector2(12, 3),
                cargo_pos=Vector2(0, 0),
                goal_pos=Vector2(12, 12), #goal_pos=Vector2(12, 12),
                has_cargo=False,
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 1)
            ),
            GenericStage(
                map_path="maps/map_tutorial2.txt",
                drone_pos=Vector2(4, 4),
                cargo_pos=Vector2(0, 0),
                goal_pos=Vector2(4, 12), # goal_pos=Vector2(4, 12),
                has_cargo=False,
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 2)
            ),
            GenericStage(
                map_path="maps/map_tutorial3.txt",
                drone_pos=Vector2(12, 3.5),
                cargo_pos=Vector2(12, 2.2),
                goal_pos=Vector2(12, 10), # goal_pos=Vector2(12, 10),
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 3)
            ),
            GenericStage(
                map_path="maps/map_tutorial4.txt",
                drone_pos=Vector2(3, 3),
                cargo_pos=Vector2(3, 1.2),
                goal_pos=Vector2(3, 8), # goal_pos=Vector2(20, 8),
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 4)
            ),
            GenericStage(
                map_path="maps/map_stage1.txt",
                drone_pos=Vector2(2, 1.5),
                cargo_pos=Vector2(21.5, 1.2),
                goal_pos=Vector2(7, 8.5), # goal_pos=Vector2(7, 8.5),
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 5)
            ),
            GenericStage(
                map_path="maps/map_stage2.txt",
                drone_pos=Vector2(3, 1.5),
                cargo_pos=Vector2(22, 10.2),
                goal_pos=Vector2(21.5, 1.5), #goal_pos=Vector2(21.5, 1.5),
                goal_condition="DRONE_ONLY",
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 6)
            ),
            StageStaticWind(
                map_path="maps/map_stage3.txt",
                drone_pos=Vector2(3.0, 3.0),
                cargo_pos=Vector2(3.0, 1.0),
                goal_pos=Vector2(2.0, 3.0),
                goal_condition="CARGO_ONLY",
                has_cargo=True,
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 7)
            ),
            StageRandomWind(
                map_path="maps/map_stage4.txt",
                drone_pos=Vector2(3.0, 3.0),
                cargo_pos=Vector2(3.0, 1.0),
                goal_pos=Vector2(2.0, 3.0),
                goal_condition="CARGO_ONLY",
                has_cargo=True,
                goal_event=lambda : EventManager.publish("CHANGE_STAGE", 8)
            )
        ]

        self.start_messages_data : list[list[tuple[float, str]]] = [
            [(1.0, "W키를 눌러 상승")],
            [(1.0, "A/S를 눌러 좌우 회전")],
            [(1.0, "R키를 눌러 화물 집기")],
            [(1.0, "E/Q키를 눌러 길이 조절")],
            [(1.0, "Stage 1 : 기초 응용")],
            [(1.0, "Stage 2 : 주행 연습")],
            [(1.0, "Stage 3 : 정적 바람")],
            [
                (1.0, "Stage 4 : 강풍 환경"),
                (1.0, "축하합니다!"),
                (1.5, "Stage 3을 클리어하셨군요!"),
                (1.0, "하지만 아쉽게도 현실은..."),
                (1.0, "게임처럼 간단하지 않습니다."),
                (1.5, "수많은 요소들이 상호작용하고,"),
                (1.5, "예측할 수 없는 일들이 일어나죠."),
                (1.5, "마침 바람이 불어오는군요..."),
                (1.0, "상하좌우 어디로든요."),
                (1.0, "과연 당신은"),
                (1.2, "자연과 맞설 수 있을까요?"),
            ],
        ]

        self.current_timeline = []
        self.map_names = ["튜토리얼 1", "튜토리얼 2", "튜토리얼 3", "튜토리얼 4", "기초 응용 구역", "주행 연습 구역", "고정 풍속 구역", "변칙 돌풍 구역"]
        self.mission_types = ["드론 이동", "기체 회전", "화물 운송", "길이 조절", "기초 화물 운송", "중급 화물 운송", "고급 화물 운송", "돌풍 속 화물 운송"]

        #region UI 구성
        self.ui_manager = UIManager()

        big_font = pygame.font.SysFont("malgungothic", 70)
        info_font = pygame.font.SysFont("malgungothic", 30)

        # 시작 메시지
        self.overlay_image = UIImage(0, 0, pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA))
        self.overlay_image.image.fill((0, 0, 0, 128)) 
        self.start_message_text = UIText(0, 0, self.start_messages_data[0][0][1], big_font, (255, 255, 255))
        self.start_message_text.center = (WIDTH//2, HEIGHT//2)

        # 게임 화면 디스플레이
        self.bg_image = UIImage(20, 20, pygame.Surface((450, 150), pygame.SRCALPHA))
        self.bg_image.image.fill((0, 0, 0, 160))
        self.holding_text = UIText(30, 30, "상태: ...", info_font, (255, 255, 255))
        self.map_info_text = UIText(30, 70, "맵 정보: ...", info_font, (255, 255, 255))
        self.mission_type_text = UIText(30, 110, "미션: ...", info_font, (255, 255, 255))
        
        # ui_manager 추가
        self.ui_manager.set([
            self.overlay_image,
            self.bg_image,
            self.start_message_text,
            self.holding_text,
            self.map_info_text,
            self.mission_type_text,
        ])
        #endregion
        
        self.total_time = 0.0
        self.total_distance = 0.0
        self.total_collision_time = 0.0
        self.total_energy_used = 0.0

        self.ui_timer = self.start_messages_data[0][0][0]

        self.current_stage_idx = 0
        self.current_stage = self.stages[0]

        EventManager.subscribe("CHANGE_STAGE", self.change_stage)
        EventManager.subscribe("FAIL_STAGE", self.fail_stage)
        EventManager.subscribe("COLLECT_INFO", self.collect_info)
        EventManager.subscribe("SET_HOLDING_TEXT", self.set_holding_text)

        self.change_stage(0)

    #region published events
    def change_stage(self, stage_num : int):
        self.current_stage_idx = stage_num 
        if self.current_stage_idx >= len(self.stages):
            EventManager.publish("CHANGE_SCENE", "END_SCENE")
            self._publish_end_scene_info(True, "모든 단계 성공!")
        else:
            self.current_stage = self.stages[self.current_stage_idx]
            self.current_timeline = list(self.start_messages_data[self.current_stage_idx])
            if self.current_timeline:
                delay, text_line = self.current_timeline.pop(0)
                self.ui_timer = delay
                
                self.overlay_image.visible = True
                self.start_message_text.set_text(text_line)
                self.start_message_text.center = (WIDTH // 2, HEIGHT // 2)
            else:
                self.ui_timer = 0.0

        self.map_info_text.set_text(f"맵 정보: {self.map_names[self.current_stage_idx]}")
        self.mission_type_text.set_text(f"미션: {self.mission_types[self.current_stage_idx]}")

    def fail_stage(self, ending_type : str):
        EventManager.publish("CHANGE_SCENE", "END_SCENE")
        self._publish_end_scene_info(False, ending_type)

    def collect_info(self, data : dict):
        ''' 
        displacement : float
        collision_time : float
        energy_used : float
        '''
        self.total_distance += data.get("displacement", 0.0)
        self.total_collision_time += data.get("collision_time", 0.0)
        self.total_energy_used += data.get("energy_used", 0.0)

    def set_holding_text(self, is_holding : bool):
        status_str = "화물 운송 중" if is_holding else "대기 중"
        self.holding_text.set_text("상태: " + status_str)
    #endregion

    def _publish_end_scene_info(self, status, ending_type : str):
        EventManager.publish("SET_END_SCENE_INFO", {
            "success" : status,
            "type" : ending_type,
            "stats" : FlightStats(
                controller= "",
                flight_time = self.total_time, 
                distance = self.total_distance, 
                collision_time = self.total_collision_time, 
                energy_used = self.total_energy_used, 
                score = self._calculate_score(),
            )
        })

    def _calculate_score(self) -> int:
        base_score = 10000
        time_penalty = max(0, int(self.total_time * 50))
        energy_penalty = max(0, int(self.total_energy_used * 10))
        collision_penalty = max(0, int(self.total_collision_time * 500))
        final_score = base_score - time_penalty - energy_penalty - collision_penalty
        return max(0, final_score)
    def update(self, dt):
        if self.ui_timer > 0:
            self.ui_timer -= dt
            if self.ui_timer <= 0:
                if self.current_timeline:
                    next_delay, next_text = self.current_timeline.pop(0)
                    self.ui_timer = next_delay
                    
                    self.start_message_text.set_text(next_text)
                    self.start_message_text.center = (WIDTH // 2, HEIGHT // 2)
                else:
                    self.start_message_text.set_text("")
                    self.overlay_image.visible = False
        else:       
            self.total_time += dt
            self.current_stage.update(dt)
        self.ui_manager.update(dt)

    def render(self, screen):
        self.current_stage.render(screen)
        self.ui_manager.render(screen)

    def __del__(self):
        '''EventManager로 인한 메모리 누수 방지'''
        try:
            EventManager.unsubscribe("CHANGE_STAGE", self.change_stage)
            EventManager.unsubscribe("FAIL_STAGE", self.fail_stage)
            EventManager.unsubscribe("COLLECT_INFO", self.collect_info)
            EventManager.unsubscribe("SET_HOLDING_TEXT", self.set_holding_text)
        except (ValueError, AttributeError):
            pass