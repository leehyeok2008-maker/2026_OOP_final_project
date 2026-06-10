import cv2
import pygame

from scenes.scene import Scene
from scenes.game_scene import GameScene


class StartScene(Scene):

    def __init__(self, app):

        super().__init__(app)

        # 배경 영상
        self.video = cv2.VideoCapture(
            "assets/videos/drone.mp4"
        )

        # 제목
        self.title_font = pygame.font.Font(
            None,
            100
        )

        # 버튼
        self.button_rect = pygame.Rect(
            540,
            500,
            200,
            60
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

        # 영상 프레임 읽기
        success, frame = self.video.read()

        if not success:

            self.video.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )

            success, frame = self.video.read()

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame = pygame.surfarray.make_surface(
            frame.swapaxes(0, 1)
        )

        frame = pygame.transform.scale(
            frame,
            screen.get_size()
        )

        screen.blit(frame, (0, 0))

        # 반투명 검은 오버레이
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 120))

        screen.blit(overlay, (0, 0))

        # 제목
        title = self.title_font.render(
            "드론 시뮬레이터",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(640, 200)
        )

        screen.blit(
            title,
            title_rect
        )

        # 버튼
        pygame.draw.rect(
            screen,
            (40, 120, 255),
            self.button_rect,
            border_radius=10
        )

        button_font = pygame.font.Font(
            None,
            40
        )

        button_text = button_font.render(
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