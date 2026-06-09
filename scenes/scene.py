from pygame import Surface
from abc import ABC, abstractmethod

class Scene(ABC):
    @abstractmethod
    def update(self, dt : float) -> None:
        pass

    @abstractmethod
    def render(self, screen : Surface) -> None:
        pass