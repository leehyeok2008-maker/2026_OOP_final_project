from pygame import Surface
from .ui_object import UIObject


class UIImage(UIObject):
    def __init__(self, x : int, y : int, image : Surface):
        super().__init__(
            x, y,
            image.get_width(),
            image.get_height()
        )

        self.image = image

    def render(self, screen: Surface):
        if not self.visible:
            return

        screen.blit(
            self.image,
            (self.x, self.y)
        )