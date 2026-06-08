from scenes.scene import Scene
import pygame


class EndScene(Scene):

    def __init__(self, app, success, stats):

        super().__init__(app)

        self.success = success
        self.stats = stats

        self.title = (
            "MISSION COMPLETE"
            if success
            else "MISSION FAILED"
        )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # R : 재시작
            if event.key == pygame.K_r:
                from scenes.game_scene import GameScene
                self.app.change_scene(
                    GameScene(self.app)
                )

            # M : 메인메뉴
            elif event.key == pygame.K_m:
                from scenes.start_scene import StartScene
                self.app.change_scene(
                    StartScene(self.app)
                )

    def update(self, dt):
        pass

    def render(self, screen):

        screen.fill((30, 30, 30))

        font_big = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 40)

        y = 100

        lines = [
            self.title,
            "",
            f"Controller : {self.stats.controller}",
            f"Flight Time : {self.stats.flight_time:.1f} s",
            f"Distance : {self.stats.distance:.1f} m",
            f"Collisions : {self.stats.collisions}",
            f"Energy Used : {self.stats.energy_used:.1f} %",
            f"Score : {self.stats.score}",
            "",
            "[R] Restart",
            "[M] Main Menu"
        ]

        for i, text in enumerate(lines):

            font = font_big if i == 0 else font_small

            surface = font.render(
                text,
                True,
                (255, 255, 255)
            )

            screen.blit(surface, (100, y))
            y += 50


class FlightStats:

    def __init__(self):

        self.controller = "Manual"

        self.flight_time = 0.0

        self.distance = 0.0

        self.collisions = 0

        self.energy_used = 0.0

        self.score = 0


self.app.change_scene(
    EndScene(
        self.app,
        success=True,
        stats=self.stats
    )
)