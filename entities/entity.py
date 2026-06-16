import math
import pygame
from pygame import Vector2
from utils import conversion
from pygame import Surface
from abc import ABC, abstractmethod
from physics import Transform, Collider, RigidBody2D
class Entity(ABC):
    def __init__(self, sprite : Surface, transform : Transform, collider : Collider):
        '''
        엔티티 추상 클래스

        Attributes:
            sprite (Surface):
                엔티티 이미지

            transform (Transform):
                엔티티의 위치 및 자세 정보

            collider (Collider):
                엔티티의 충돌 반경 
        '''
        self.sprite = sprite
        self.transform = transform
        self.collider = collider
        self.has_physics = True

    def update(self, dt) -> None:
        pass

    def on_collision(self, other):
        pass

    def render(self, screen : Surface, camera_pos : Vector2) -> None:
        px_size = conversion.change_meter_to_px(self.transform.size)
        scaled_sprite = pygame.transform.scale(self.sprite, px_size)
        scaled_sprite = scaled_sprite.convert_alpha()
        angle_deg = math.degrees(self.transform.angle)
        rotated_sprite = pygame.transform.rotate(scaled_sprite, angle_deg)
        rotated_sprite.set_colorkey((0, 0, 0))
        rect = rotated_sprite.get_rect(
            center=conversion.calculate_pos_on_screen(self.transform.position, camera_pos, screen)
        )
        screen.blit(rotated_sprite, rect)

class StaticEntity(Entity):
    """타일, 벽, 지형 등 움직이지 않는 객체"""
    def __init__(self, sprite: Surface, transform: Transform, collider: Collider):
        super().__init__(sprite, transform, collider)

    def update(self, dt: float):
        pass

class DynamicEntity(Entity):
    """드론, 플레이어, 적 등 물리 연산이 필요한 객체"""
    def __init__(
        self, 
        sprite: Surface, 
        transform: Transform, 
        collider: Collider,
        mass: float,
        moment: float | None = None, 
        velocity : Vector2 | None = None,
        angular_velocity : float = 0.0,
    ):
        super().__init__(sprite, transform, collider)
            
        self.rigidbody = RigidBody2D(transform, mass, moment, velocity or Vector2(0, 0), angular_velocity)

    def update(self, dt: float):
        self.rigidbody.update(dt)