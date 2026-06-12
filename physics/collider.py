import math
from pygame import Vector2
from .transform import Transform
class Collider:
    def __init__(self, transform : Transform, offset : Vector2 | None = None):
        self.transform = transform
        self.offset = offset or Vector2(0, 0)

    @property
    def position(self):
        return self.transform.position + self.transform.transform_absolute_vector(self.offset)

class RectCollider(Collider):
    def __init__(
        self, width : float, height : float,
        transform : Transform, offset : Vector2 | None = None,
    ):
        super().__init__(transform, offset)
        self.width = width
        self.height = height

    @property
    def width_vector(self) -> Vector2:
        w_x = self.width * math.cos(self.transform.angle) / 2
        w_y = self.width * math.sin(self.transform.angle) / 2
        return Vector2(w_x, w_y)
    @property
    def height_vector(self) -> Vector2:
        h_x = -self.height * math.sin(self.transform.angle) / 2
        h_y = self.height * math.cos(self.transform.angle) / 2
        return Vector2(h_x, h_y)
        
class CircleCollider(Collider):
    def __init__(
        self, radius: float,
        transform: Transform, offset: Vector2 | None = None
    ):
        super().__init__(transform, offset)
        self.radius = radius

    