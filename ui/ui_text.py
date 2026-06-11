from pygame import Surface
from pygame.font import Font
from .ui_object import UIObject

class UIText(UIObject):
    def __init__(self, 
        x : int, y : int, 
        text : str, 
        font : Font, 
        color=(0, 0, 0),
    ):
        self.text = text
        self.font = font
        self.color = color

        surface = font.render(text, True, color)

        super().__init__(
            x, y,
            surface.get_width(),
            surface.get_height()
        )

    def set_text(self, text : str):
        self.text = text

    def render(self, screen : Surface):
        if not self.visible:
            return
        
        surface = self.font.render(self.text, True, self.color)

        self.width = surface.get_width()
        self.height = surface.get_height()

        screen.blit(
            surface,
            (self.x, self.y)
        )