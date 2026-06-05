from abc import ABC, abstractmethod
class Controller(ABC):
    @abstractmethod
    def command(self, input) -> list[str]:
        return []

    def __call__(self, input) -> list[str]:
        return self.command(input)