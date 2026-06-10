from scenes.scene import Scene

from stages.stage1 import Stage1
from stages.stage2 import Stage2
from stages.stage3 import Stage3

from scenes.end_scene import EndScene


class GameScene(Scene):

    def __init__(self, app):

        super().__init__(app)

        self.stages = [
            Stage1(),
            Stage2(),
            Stage3()
        ]

        self.current_stage_idx = 0
        self.current_stage = self.stages[0]

    def handle_event(self, event):

        self.current_stage.handle_event(event)

    def update(self, dt):

        result = self.current_stage.update(dt)

        if result == "CLEAR":

            self.current_stage_idx += 1

            # 모든 스테이지 클리어
            if self.current_stage_idx >= len(self.stages):

                self.app.change_scene(
                    EndScene(
                        self.app,
                        success=True
                    )
                )

            # 다음 스테이지 이동
            else:

                self.current_stage = \
                    self.stages[self.current_stage_idx]

        elif result == "FAIL":

            self.app.change_scene(
                EndScene(
                    self.app,
                    success=False
                )
            )

    def render(self, screen):

        self.current_stage.render(screen)