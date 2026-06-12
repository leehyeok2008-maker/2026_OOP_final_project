from pygame import Surface, Vector2
from abc import ABC, abstractmethod
from entities import *
from managers import ColliderManager

class Stage(ABC):
    def __init__(self, drone : Drone, cargo : Cargo, map):
        self.drone = drone
        self.cargo = cargo
        self.map = map
        self.grav_acc = Vector2(0, -9.8)
        self.collider_manager = ColliderManager()
        self.collider_manager.register(self.drone, self.drone.collider)
        self.collider_manager.register(self.cargo, self.cargo.collider)
        
    def update(self, dt : float):
        self.drone.rigidbody.apply_force(self.grav_acc)
        self.cargo.rigidbody.apply_force(self.grav_acc)
        self.drone.update(dt)
        self.cargo.update(dt)

    def render(self, screen : Surface):
        self.drone.render(screen)
        self.cargo.render(screen)
        pass
