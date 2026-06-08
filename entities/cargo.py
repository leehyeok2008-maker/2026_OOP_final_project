from pygame import Vector2, Surface
from entity import Entity
from physics.rigidbody2d import RigidBody2D

class Cargo(Entity):
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
        self.rigidbody.update(dt)
        return []
        