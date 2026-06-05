from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    # 선택사항
    def enter(self):
        pass

    def exit(self):
        pass