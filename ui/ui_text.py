from pygame import Surface
from pygame.font import Font
from .ui_object import UIObject

class UIText(UIObject):
    def __init__(self, 
        x : int, y : int, 
        text : str, 
        font : Font, 
        color=(0, 0, 0),
        line_spacing : int = 0
    ):
        self.text = text
        self.font = font
        self.color = color
        self.line_spacing = line_spacing

        width, height = self._calculate_dimensions(text, font, line_spacing)

        super().__init__(x, y, width, height)
    
    def _calculate_dimensions(self, text: str, font: Font, line_spacing: int):
        '''줄 바꿈 고려해서 크기 계산'''
        lines = text.split('\n')
        max_width = 0
        line_height = font.get_linesize() + line_spacing
        total_height = line_height * len(lines)

        for line in lines:
            # 텍스트 길이를 알아내기 위해 렌더링
            surface = font.render(line, True, self.color)
            if surface.get_width() > max_width:
                max_width = surface.get_width()
                
        return max_width, total_height
    
    def set_text(self, text : str):
        self.text = text

    def render(self, screen : Surface):
        if not self.visible:
            return
        
        lines = self.text.split('\n')
        max_width = 0
        line_height = self.font.get_linesize() + self.line_spacing
        current_y = self.y

        for line in lines:
            surface = self.font.render(line, True, self.color)
            screen.blit(surface, (self.x, current_y))
            if surface.get_width() > max_width:
                max_width = surface.get_width()
                
            current_y += line_height

        self.width = max_width
        self.height = current_y - self.y