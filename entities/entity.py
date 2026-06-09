import math
import pygame
from pygame import Surface
from abc import ABC, abstractmethod
from physics.transform import Transform
class Entity(ABC):
    def __init__(self, sprite : Surface, transform : Transform):
        '''
        엔티티 추상 클래스

        Attributes:
            sprite (Surface):
                엔티티 이미지

            transform (Transform):
                엔티티의 위치 및 자세 정보
        '''
        self.sprite = sprite
        self.transform = transform
        
    @abstractmethod
    def update(self, dt) -> list[str]:
        return []

    def render(self, screen) -> None:
        angle_deg = math.degrees(self.transform.angle)
        rotated_sprite = pygame.transform.rotate(self.sprite, angle_deg)
        rect = rotated_sprite.get_rect(center=self.transform.position)
        screen.blit(rotated_sprite, rect)
