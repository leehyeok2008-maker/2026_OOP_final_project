import math
from pygame import Vector2, Rect
from .transform import Transform
class Collider:
    def __init__(self, transform : Transform, offset : Vector2 | None = None):
        self.transform = transform
        self.offset = offset or Vector2(0, 0)
        self.max_distance = math.sqrt(transform.size[0] ** 2 + transform.size[1] ** 2) # 충돌을 확인하는 최대 거리

    @property
    def position(self):
        return self.transform.position + self.transform.transform_absolute_vector(self.offset)


class RectCollider(Collider):
    def __init__(
        self, width : float, height : float,
        transform : Transform, offset : Vector2 | None = None,
    ):
        super().__init__(transform, offset)
        self.max_distance = math.sqrt(width**2 + height**2) 
        self.width = width
        self.height = height

    @property
    def width_vector(self) -> Vector2:
        ''' 너비 절반 크기의 수직 벡터'''
        w_x = self.width * math.cos(self.transform.angle) / 2
        w_y = self.width * math.sin(self.transform.angle) / 2
        return Vector2(w_x, w_y)
    @property
    def height_vector(self) -> Vector2:
        ''' 높이 절반 크기의 수직 벡터'''
        h_x = -self.height * math.sin(self.transform.angle) / 2
        h_y = self.height * math.cos(self.transform.angle) / 2
        return Vector2(h_x, h_y)
    