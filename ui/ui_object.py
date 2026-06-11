from pygame import Surface
from abc import ABC, abstractmethod
class UIObject(ABC):
    def __init__(self, x : int, y : int, width : int, height : int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True

    #region 프로퍼티
    @property
    def pos(self):
        return (
            self.x,
            self.y
        )

    @pos.setter
    def pos(self, pos):
        x, y = pos
        self.x = x
        self.y = y

    @property
    def center_x(self):
       return self.x + self.width // 2

    @center_x.setter
    def center_x(self, value):
        self.x = value - self.width // 2


    @property
    def center_y(self):
        return self.y + self.height // 2

    @center_y.setter
    def center_y(self, value):
        self.y = value - self.height // 2

    @property
    def center(self):
        return (
            self.center_x,
            self.center_y
        )

    @center.setter
    def center(self, pos):
        cx, cy = pos
        self.center_x = cx
        self.center_y = cy
    #endregion

    def update(self, dt):
        pass
        
    @abstractmethod
    def render(self, screen : Surface):
        pass

    def contain(self, px : int, py : int) -> bool:
        return (self.x <= px <= (self.x + self.width)) and (self.y <= py <= (self.y + self.height))


