class Stage1:

    def __init__(self):

        self.tutorial_step = 0

    def update(self, dt):

        if self.tutorial_step == 0:

            if self.drone.position.y < 300:
                self.tutorial_step = 1

        elif self.tutorial_step == 1:

            if self.left_target_reached:
                self.tutorial_step = 2

        elif self.tutorial_step == 2:

            if self.cargo_attached:
                self.tutorial_step = 3

        elif self.tutorial_step == 3:

            if self.goal_reached:
                return "CLEAR"

    def get_tutorial_text(self):

        texts = [

            "~ 키를 눌러 상승.",

            "~ 키를 눌러 좌우이동.",

            "화물 위로 이동하세요.",

            "화물을 목적지까지 운반하세요."
        ]

        return texts[self.tutorial_step]


    def render(self, screen):

        text = font.render(
            self.get_tutorial_text(),
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 20))
