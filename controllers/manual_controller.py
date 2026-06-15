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
            right_input += self.drone.max_right_thrust * 0.5
            
        if InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_RIGHT):
            left_input += self.drone.max_left_thrust * 0.5

        if InputManager.is_key_pressed(pygame.K_r):
            self.drone.is_trying_to_hold = True
        else:
            self.drone.is_trying_to_hold = False

        if InputManager.is_key_down(pygame.K_e):
            self.drone.rope_length += self.drone.rope_speed * dt
            print(self.drone.rope_length)
        
        if InputManager.is_key_down(pygame.K_q):
            self.drone.rope_length -= self.drone.rope_speed * dt

        self.drone.set_thrust(left_input, right_input)
        
