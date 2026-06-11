from abc import ABC, abstractmethod
from entities.drone import Drone

class Controller(ABC):
    def __init__(self, drone : Drone):
        self.drone : Drone = drone
        
    @abstractmethod
    def command(self, input):
        pass

    def __call__(self, input):
       self.command(input)