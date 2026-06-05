import math
import pygame
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

    def render(self, screen) -> None:
        angle_deg = math.degrees(self.rigidbody.angle)
        rotated_sprite = pygame.transform.rotate(self.sprite, angle_deg)
        rect = rotated_sprite.get_rect(center=self.rigidbody.position)
        screen.blit(rotated_sprite, rect)
