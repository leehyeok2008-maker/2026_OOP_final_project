import pygame

from config import *
from pygame import Surface
from scenes.scene import Scene
from managers import UIManager, EventManager
from ui import UIText, UIButton


class StartScene(Scene):
    def __init__(self):
        
        self.ui_manager = UIManager()

        title_font = pygame.font.SysFont("malgungothic", 100)
        button_font = pygame.font.SysFont("malgungothic", 50)
        info_font = pygame.font.SysFont("malgungothic", 30)

        self.title_text = UIText(
                0,
                0,
                "드론 시뮬레이터",
                title_font
            )
        self.title_text.center = (WIDTH//2, HEIGHT//2)

        self.start_button = UIButton(
                0,
                0,
                200,
                70,
                "시작하기",
                button_font,
                callback=lambda : EventManager.publish("CHANGE_SCENE", "GAME_SCENE")
            )
        self.start_button.center = (WIDTH//2, HEIGHT//2 + 100)

        self.description_text = UIText(
                0,
                0,
                "시작하기 버튼을 클릭하세요.",
                info_font,
                (180, 180, 180)
            )
        self.description_text.center = (WIDTH//2, HEIGHT//2 + 200)

        self.ui_manager.set([
            self.title_text,
            self.description_text,
            self.start_button,
        ])
    

    def update(self, dt):
        self.ui_manager.update(dt)

    def render(self, screen : Surface):
        self.ui_manager.render(screen)