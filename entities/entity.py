from pygame import Vector2, Surface
from abc import ABC, abstractmethod
from physics.rigidbody2d import RigidBody2D
class Entity(ABC):
    def __init__(self, sprite : Surface, rigidbody : RigidBody2D):
        self.sprite = sprite
        self.rigidbody = rigidbody
        
    @abstractmethod
    def update(self, dt) -> list[str]:
        return []

    @abstractmethod
    def render(self, screen) -> None:
        return 
