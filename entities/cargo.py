from pygame import Vector2, Surface
from .entity import Entity
from physics.transform import Transform
from physics.rigidbody2d import RigidBody2D
from physics.collider import RectCollider

class Cargo(Entity):
    def __init__(
        self, size : tuple[float, float], sprite : Surface, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0
    ):
        transform=Transform(position or Vector2(0, 0), angle, size)
        super().__init__(
            sprite=sprite,
            transform=transform,
            collider=RectCollider(50, 50, transform)
        )
        self.rigidbody = RigidBody2D(mass, moment, self.transform, velocity or Vector2(0, 0), angular_velocity)

    def update(self, dt):
        self.rigidbody.update(dt)
        