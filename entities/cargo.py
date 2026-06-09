from pygame import Vector2, Surface
from entity import Entity
from physics.transform import Transform
from physics.rigidbody2d import RigidBody2D

class Cargo(Entity):
    def __init__(
        self, sprite : Surface, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0
    ):
        super().__init__(
            sprite=sprite,
            transform=Transform(Vector2(0, 0) if position is None else position, angle)
        )
        self.rigidbody = RigidBody2D(mass, moment, self.transform, Vector2(0, 0) if velocity is None else velocity, angular_velocity)

    def update(self, dt) -> None:
        self.rigidbody.update(dt)
        