import pygame
from config import *
from entities import *
from utils import conversion
from pygame import Surface, Vector2
from abc import ABC, abstractmethod
from controllers import Controller
from managers import ColliderManager

class Stage(ABC):
    def __init__(self, drone : Drone, cargo : Cargo, map : TileMap, controller : Controller):
        self.drone = drone
        self.cargo = cargo
        self.map = map
        self.controller = controller
        self.grav_acc = Vector2(0, -9.8)
        self.air_resistance = 0.05
        self.collider_manager = ColliderManager()
        self.collider_manager.register(self.drone, self.drone.collider)
        self.collider_manager.register(self.cargo, self.cargo.collider)
        self.collider_manager.register_all([(e, e.collider) for e in self.map.get_tiles()])
        self.camera_pos = conversion.change_px_to_meter(Vector2(WIDTH - DEFAULT_PX_PER_METER, HEIGHT - DEFAULT_PX_PER_METER))/2

    def update(self, dt : float):
        self.collider_manager.check_all()
        self.drone.rigidbody.apply_force(self.drone.rigidbody.mass * self.grav_acc)
        self.cargo.rigidbody.apply_force(self.drone.rigidbody.mass * self.grav_acc)
        self.drone.rigidbody.apply_force(-self.drone.left_velocity *  self.air_resistance)
        self.cargo.rigidbody.apply_force(-self.drone.right_velocity * self.air_resistance)
        self.controller.command(dt)
        self.drone.update(dt)
        self.cargo.update(dt)

        self.update_rope()

    def render(self, screen : Surface):
        self.drone.render(screen, self.camera_pos)
        self.cargo.render(screen, self.camera_pos)
        self.map.render(screen, self.camera_pos)
        self.render_rope(screen, self.camera_pos)

    #region rope 코드
    def update_rope(self):
        cargo = self.drone.attached_cargo
        if cargo is None or not self.drone.is_holding: return
        
        anchor_point = self.drone.anchor_point
        to_cargo = cargo.transform.position - anchor_point
        current_distance = to_cargo.length()
        current_length = self.drone.rope_length
        if current_distance > current_length:
            rope_dir = to_cargo.normalize()
            self.cargo.transform.position = anchor_point + rope_dir * current_length

            relative_velocity = cargo.rigidbody.velocity - self.drone.rigidbody.velocity
            vel_along_rope = relative_velocity.dot(rope_dir)

            # 화물의 바깥 방향 속도 차단
            if vel_along_rope > 0:
                    cargo.rigidbody.velocity -= rope_dir * vel_along_rope

                    total_mass = self.drone.rigidbody.mass + cargo.rigidbody.mass
                    drone_pull_factor = cargo.rigidbody.mass / total_mass
                    
                    # 드론의 속도도 화물이 당기는 방향(rope_dir)으로 변환시킵니다.
                    self.drone.rigidbody.velocity += rope_dir * vel_along_rope * drone_pull_factor

    def render_rope(self, screen, camera_pos : Vector2):
        cargo = self.drone.attached_cargo
        if cargo is None or not self.drone.is_holding: return

        anchor_point = self.drone.anchor_point
        cargo_center = cargo.transform.position

        start_px = conversion.calculate_pos_on_screen(anchor_point, camera_pos, screen)
        end_px = conversion.calculate_pos_on_screen(cargo_center, camera_pos, screen)
            
        rope_color = (50, 50, 50)
        rope_thickness = 4
            
        pygame.draw.line(screen, rope_color, start_px, end_px, rope_thickness)
    #endregion