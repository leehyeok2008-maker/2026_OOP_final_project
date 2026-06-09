from pygame import Surface, Vector2
from abc import ABC, abstractmethod
from entities.drone import Drone
from entities.cargo import Cargo

class Stage(ABC):
    def __init__(self, drone : Drone, cargo : Cargo, map):
        self.drone = drone
        self.cargo = cargo
        self.map = map
        self.grav_acc = Vector2(0, -9.8)

    def update(self, dt : float) -> list[str]:
        self.drone.rigidbody.apply_force(self.grav_acc)
        self.cargo.rigidbody.apply_force(self.grav_acc)
        
        self.drone.update(dt)
        self.cargo.update(dt)
        return []

    def render(self, screen : Surface) -> None:
        self.drone.render(screen)
        self.cargo.render(screen)
        pass
