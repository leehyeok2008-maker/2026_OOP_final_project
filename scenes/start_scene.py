import pygame

from scenes.scene import Scene
from scenes.game_scene import GameScene


class StartScene(Scene):

    def __init__(self, app):

        super().__init__(app)

        self.title_font = pygame.font.Font(
            None,
            100
        )

        self.button_font = pygame.font.Font(
            None,
            50
        )

        self.button_rect = pygame.Rect(
            540,
            450,
            200,
            70
        )

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.button_rect.collidepoint(
                event.pos
            ):

                self.app.change_scene(
                    GameScene(self.app)
                )

    def update(self, dt):
        pass

    def render(self, screen):

        # 검은 배경
        screen.fill((0, 0, 0))

        # 제목
        title = self.title_font.render(
            "드론 시뮬레이터",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(640, 220)
        )

        screen.blit(
            title,
            title_rect
        )

        # 제목 아래 선
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (300, 300),
            (980, 300),
            2
        )

        # 버튼
        pygame.draw.rect(
            screen,
            (40, 120, 255),
            self.button_rect,
            border_radius=10
        )

        # 버튼 텍스트
        button_text = self.button_font.render(
            "시작하기",
            True,
            (255, 255, 255)
        )

        button_text_rect = button_text.get_rect(
            center=self.button_rect.center
        )

        screen.blit(
            button_text,
            button_text_rect
        )

        # 설명
        info_font = pygame.font.Font(
            None,
            30
        )

        info_text = info_font.render(
            "시작하기 버튼을 클릭하세요.",
            True,
            (180, 180, 180)
        )

        info_rect = info_text.get_rect(
            center=(640, 600)
        )

        screen.blit(
            info_text,
            info_rect
        )