import pygame
from .scene import Scene
from .stats import FlightStats

from stages import Stage, Stage1, Stage2, Stage3
from managers import UIManager, EventManager
from ui import UIText


class GameScene(Scene):

    def __init__(self):

        self.stages : list[Stage] = [
            Stage1(),
            Stage2(),
            Stage3(),
        ]

        #region UI 구성
        self.ui_manager = UIManager()

        title_font = pygame.font.SysFont("malgungothic", 100)
        button_font = pygame.font.SysFont("malgungothic", 50)
        info_font = pygame.font.SysFont("malgungothic", 30)
        #endregion

        self.total_time = 0.0
        self.total_distance = 0.0
        self.total_collision_time = 0.0
        self.total_energy_used = 0.0
        self.current_stage_idx = 0
        self.current_stage = self.stages[0]
        EventManager.subscribe("CHANGE_STAGE", self.change_stage)
        EventManager.subscribe("COLLECT_INFO", self.collect_info)

    def change_stage(self, stage_num : int):
        self.current_stage_idx = stage_num 
        if self.current_stage_idx >= len(self.stages):
            EventManager.publish("CHANGE_SCENE", "END_SCENE")
            EventManager.publish("SET_END_SCENE_INFO", {
                "success" : True,
                "stats" : FlightStats(
                    controller = "나중에 추가",
                    flight_time = self.total_time, 
                    distance = self.total_distance, 
                    collision_time = self.total_collision_time, 
                    energy_used = self.total_energy_used, 
                    score = self._calculate_score(),
                )
            })
        else:
            self.current_stage = self.stages[self.current_stage_idx]

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
        self.total_time += dt
        self.current_stage.update(dt)
        self.ui_manager.update(dt)

    def render(self, screen):
        self.current_stage.render(screen)
        self.ui_manager.render(screen)