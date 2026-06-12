from typing import overload
from pygame import Surface
from pygame.math import Vector2
from config import *

@overload
def change_meter_to_px(val: float) -> float: ...

@overload
def change_meter_to_px(val: Vector2) -> Vector2: ...

@overload
def change_meter_to_px(val : tuple[float, float]) -> tuple[float, float]: ...

def change_meter_to_px(val: float | Vector2 | tuple[float, float]) -> float | Vector2 | tuple[float, float]:
    '''미터(SI)를 픽셀(Pixel)로 변환.'''
    if isinstance(val, tuple):
        return (val[0] * DEFAULT_PX_PER_METER, val[1] * DEFAULT_PX_PER_METER)
    return val * DEFAULT_PX_PER_METER


@overload
def change_px_to_meter(val: float) -> float: ...

@overload
def change_px_to_meter(val: Vector2) -> Vector2: ...

@overload
def change_px_to_meter(val : tuple[float, float]) -> tuple[float, float]: ...

def change_px_to_meter(val: float | Vector2 | tuple[float, float]) -> float | Vector2 | tuple[float, float]:
    '''픽셀(Pixel)을 미터(SI)로 변환.'''
    if isinstance(val, tuple):
        return (val[0] / DEFAULT_PX_PER_METER, val[1] / DEFAULT_PX_PER_METER)
    return val / DEFAULT_PX_PER_METER

def calculate_pos_on_screen(pos : Vector2, cam : Vector2, screen : Surface) -> tuple[int, int]:
    relative_pos = pos - cam
    pixel_position = change_meter_to_px(relative_pos)
    px_x = int(pixel_position.x)
    px_y = -int(pixel_position.y)
    return (px_x + screen.get_width()//2, px_y + screen.get_height()//2)
