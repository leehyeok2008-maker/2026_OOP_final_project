from pygame import Vector2, Surface
from typing import Callable
from managers.event_manager import EventManager
from physics import Transform, RectCollider
from .entity import StaticEntity
from .cargo import Cargo
from .drone import Drone

class Goal(StaticEntity):
    def __init__(
        self, size : tuple[float, float], sprite : Surface, stage_num : int,
        position : Vector2 | None = None, angle : float = 0.0,
        collider_scale : tuple[float, float] = (0.5, 0.5),
        condition_type : str = "CARGO_ONLY",
        goal_event : Callable[[], None] = lambda: None,
    ):
        transform = Transform(position, angle, size)
        super().__init__(
            sprite=sprite,
            transform=transform,
            collider=RectCollider(size[0] * collider_scale[0], size[1] * collider_scale[1], transform)
        )
        self.is_solid = False
        self.stage_num = stage_num
        self.condition_type = condition_type
        self.goal_event = goal_event
    
    def on_collision(self, other):
        if self.goal_event is None: return

        is_cleared = False
        
        if self.condition_type == "CARGO_ONLY":
            if isinstance(other, Cargo):
                is_cleared = True
        elif self.condition_type == "DRONE_ONLY":
            if isinstance(other, Drone):
                is_cleared = True

        if is_cleared:
            self.goal_event()