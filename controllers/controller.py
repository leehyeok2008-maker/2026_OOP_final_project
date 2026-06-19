from abc import ABC, abstractmethod
from entities import Drone

class Controller(ABC):
    def __init__(self, drone : Drone):
        self.drone : Drone = drone
        
    @abstractmethod
    def command(self, dt : float, **kwargs) -> None:
        pass

    def __call__(self, input):
       self.command(input)

    def __str__(self):
        return "조종기"