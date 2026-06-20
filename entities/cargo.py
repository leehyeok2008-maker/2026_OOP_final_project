from pygame import Vector2, Surface
from .entity import DynamicEntity
from .tile_map import Tile
from physics.transform import Transform
from physics.rigidbody2d import RigidBody2D
from physics.collider import RectCollider
from managers.event_manager import EventManager

class Cargo(DynamicEntity):
    def __init__(
        self, size : tuple[float, float], sprite : Surface, mass : float = 1.0, moment : float | None = None, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0,
        collider_scale : tuple[float, float] = (1.0, 1.0)
    ):
        transform=Transform(position, angle, size)
        super().__init__(
            sprite=sprite,
            transform=transform,
            collider=RectCollider(size[0], size[1],  transform),
            mass=mass,
            moment=moment,
            velocity=velocity,
            angular_velocity=angular_velocity,
        )

    def update(self, dt):
        #공기저항
        self.rigidbody.velocity *= 0.97
        self.rigidbody.angular_velocity *= 0.97
        
        super().update(dt)
        