from pygame import Surface
from pygame.event import Event
from abc import ABC, abstractmethod
class Scene(ABC):
    @abstractmethod
    def handle_event(self, pg_events : list[Event]) -> None:
        pass

    @abstractmethod
    def update(self, dt : float) -> list[str]:
        pass

    @abstractmethod
    def render(self, screen : Surface) -> None:
        pass
