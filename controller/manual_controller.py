import pygame
from config import *
from managers import InputManager
from entities.drone import Drone
from .controller import Controller

class ManualController(Controller):
    def __init__(self, drone: Drone):
        super().__init__(drone)

    def command(self, input):
        commands = [] 
        if InputManager.is_key_down(pygame.K_a) or InputManager.is_key_down(pygame.K_LEFT):
            commands.append("MOVE_LEFT")
        if InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_RIGHT):
            commands.append("MOVE_RIGHT")
        if InputManager.is_key_down(pygame.K_w) or InputManager.is_key_down(pygame.K_UP):
            commands.append("MOVE_UP")
        if InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_DOWN):
            commands.append("MOVE_DOWN")
        self.drone.add_commands(commands)
        
