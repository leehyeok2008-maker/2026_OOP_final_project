from pygame import Vector2
from abc import ABC, abstractmethod
from physics.rigidbody2d import RigidBody2D
class Entity(ABC):
    def __init__(
        self, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0
    ):
        self.rigidbody = RigidBody2D(mass, moment, position, velocity, angle, angular_velocity)

    @abstractmethod
    def update(self, dt) -> list[str]:
        return []

    @abstractmethod
    def render(self, screen) -> None:
        return 
