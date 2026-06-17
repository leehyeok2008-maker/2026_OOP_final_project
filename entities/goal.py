from pygame import Vector2, Surface
from managers.event_manager import EventManager
from physics import Transform, RectCollider
from .entity import StaticEntity
from .cargo import Cargo

class Goal(StaticEntity):
    def __init__(
        self, size : tuple[float, float], sprite : Surface, stage_num : int,
        position : Vector2 | None = None, angle : float = 0.0,
        collider_scale : tuple[float, float] = (1.0, 1.0),
    ):
        transform = Transform(position, angle, size)
        super().__init__(
            sprite=sprite,
            transform=transform,
            collider=RectCollider(size[0] * collider_scale[0], size[1] * collider_scale[1], transform)
        )
        self.is_solid = False
        self.stage_num = stage_num
    
    def on_collision(self, other):
        if isinstance(other, Cargo):
            EventManager.publish("CHANGE_STAGE", self.stage_num)