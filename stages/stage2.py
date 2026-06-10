from pygame import Vector2
import pygame


class Stage2:

    def __init__(self):

        # 드론
        self.drone = Drone(
            position=Vector2(100, 300)
        )

        # 화물
        self.cargo = Cargo(
            position=Vector2(400, 300)
        )

        # 목표지점
        self.goal_pos = Vector2(800, 300)
        self.goal_radius = 30

        # 강풍
        self.wind_force = Vector2(200, 0)

        # 상태
        self.cargo_attached = False

        # 안내 문구 표시 시간
        self.message_timer = 5.0

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # E키로 화물 연결
            if event.key == pygame.K_e:

                distance = (
                    self.drone.rigidbody.transform.position
                    -
                    self.cargo.rigidbody.transform.position
                ).length()

                if distance < 50:

                    self.cargo_attached = True

    def update(self, dt):

        # 강풍 적용
        self.drone.rigidbody.apply_force(
            self.wind_force
        )

        # 드론 업데이트
        self.drone.update(dt)

        # 화물 연결 상태
        if self.cargo_attached:

            self.cargo.rigidbody.transform.position = (
                self.drone.rigidbody.transform.position
                + Vector2(0, 40)
            )

        else:

            self.cargo.update(dt)

        # 안내문 타이머
        if self.message_timer > 0:
            self.message_timer -= dt

        # 성공 판정
        if (
            self.cargo.rigidbody.transform.position
            - self.goal_pos
        ).length() <= self.goal_radius:

            return "CLEAR"

        return None

    def render(self, screen):

        # 목표 지점
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            self.goal_pos,
            self.goal_radius,
            2
        )

        # 드론
        self.drone.render(screen)

        # 화물
        self.cargo.render(screen)

        # 목표 표시
        font = pygame.font.Font(None, 30)

        text = font.render(
            "GOAL",
            True,
            (0, 255, 0)
        )

        screen.blit(
            text,
            (
                self.goal_pos.x - 20,
                self.goal_pos.y - 50
            )
        )

        # 튜토리얼 문구
        if self.message_timer > 0:

            tutorial = [
                "Stage 2 : 강풍 환경",
                "",
                "강풍이 불고 있습니다.",
                "드론이 계속 오른쪽으로 밀려납니다.",
                "",
                "화물 위로 이동하세요.",
                "E 키를 눌러 화물을 부착하세요.",
                "",
                "화물을 녹색 지점으로 운반하세요."
            ]

            y = 50

            for line in tutorial:

                text = font.render(
                    line,
                    True,
                    (255, 255, 255)
                )

                screen.blit(text, (50, y))

                y += 35

        # 상태 UI
        info = font.render(
            f"Wind : {self.wind_force.x:.0f} N ->",
            True,
            (255, 255, 255)
        )

        screen.blit(info, (20, 20))

        cargo_text = font.render(
            f"Cargo : {'Attached' if self.cargo_attached else 'Detached'}",
            True,
            (255, 255, 255)
        )

        screen.blit(cargo_text, (20, 55))