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
        self.camera_pos = conversion.change_px_to_meter(Vector2(WIDTH - DEFAULT_PX_PER_METER, HEIGHT - DEFAULT_PX_PER_METER))/2

    def update(self, dt : float):
        self.drone.rigidbody.apply_force(self.grav_acc)
        self.cargo.rigidbody.apply_force(self.grav_acc)
        self.drone.rigidbody.apply_force(-self.drone.rigidbody.velocity * self.air_resistance)
        self.cargo.rigidbody.apply_force(-self.cargo.rigidbody.velocity * self.air_resistance)
        self.controller.command(None)
        self.drone.update(dt)
        self.cargo.update(dt)

    def render(self, screen : Surface):
        self.drone.render(screen, self.camera_pos)
        self.cargo.render(screen, self.camera_pos)
        self.map.render(screen, self.camera_pos)
        pass
