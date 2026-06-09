from pygame import Surface
from abc import ABC, abstractmethod
class UIObject(ABC):
    def __init__(self, x : int, y : int, width : int, height : int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        
    @abstractmethod
    def render(self, screen : Surface) -> None:
        pass

    def contain(self, px : int, py : int) -> bool:
        return (self.x <= px <= (self.x + self.width)) and (self.y <= py <= (self.y + self.width))