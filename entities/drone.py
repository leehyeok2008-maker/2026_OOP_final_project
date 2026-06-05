import math
import pygame
from pygame import Vector2, Surface
from entity import Entity
from physics.rigidbody2d import RigidBody2D

class Drone(Entity):
    def __init__(
        self, sprite : Surface, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0
    ):
        super().__init__(
            sprite=sprite,
            rigidbody=RigidBody2D(mass, moment, position, velocity, angle, angular_velocity)
        )

    def update(self, dt) -> list[str]:
        return []
    
    def render(self, screen : Surface) -> None:
        angle_deg = math.degrees(self.rigidbody.angle)
        rotated_sprite = pygame.transform.rotate(self.sprite, angle_deg)
        rect = rotated_sprite.get_rect(center=self.rigidbody.position)
        screen.blit(rotated_sprite, rect)

        