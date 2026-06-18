import pygame
from pygame import Surface
from pygame.font import Font
from .ui_object import UIObject
from managers.input_manager import InputManager


class UIButton(UIObject):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font : Font,
        callback=None,

        bg_color=(70, 70, 70),
        text_color=(0, 0, 0),
        hover_color=(100, 100, 100),
        
        border_radius = -1,
    ):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.border_radius = border_radius

        self.is_hovering = False

    def update(self, dt):
        mx, my = InputManager.mouse_pos
        self.is_hovering = self.contain(mx, my)
        if self.is_hovering and InputManager.is_mouse_pressed(pygame.BUTTON_LEFT):
            self.on_click()

    def publish(self):
        print(self.callback)
        if self.callback:
            self.callback()

    def on_click(self):
        self.publish()

    def render(self, screen: Surface) -> None:
        if not self.visible:
            return

        color = (
            self.hover_color
            if self.is_hovering
            else self.bg_color
        )

        pygame.draw.rect(
            screen,
            color,
            (
                self.x,
                self.y,
                self.width,
                self.height
            ),
            border_radius=self.border_radius
        )

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text_surface.get_rect(
            center=(
                self.x + self.width / 2,
                self.y + self.height / 2
            )
        )

        screen.blit(
            text_surface,
            text_rect
        )