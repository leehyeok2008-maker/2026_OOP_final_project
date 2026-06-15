import pygame
from config import *
from managers import InputManager
from entities import Drone
from .controller import Controller

class ManualController(Controller):
    def __init__(self, drone: Drone):
        super().__init__(drone)

    def command(self, dt, **kwargs):
        left_input = 0.0
        right_input = 0.0
        
        if InputManager.is_key_down(pygame.K_w) or InputManager.is_key_down(pygame.K_UP):
            left_input += self.drone.max_left_thrust
            right_input += self.drone.max_right_thrust
            
        if InputManager.is_key_down(pygame.K_a) or InputManager.is_key_down(pygame.K_LEFT):
            right_input += self.drone.max_right_thrust * 0.3
            
        if InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_RIGHT):
            left_input += self.drone.max_left_thrust * 0.3

        self.drone.set_thrust(left_input, right_input)
        
