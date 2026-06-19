import pygame
from config import *
from managers import InputManager
from entities import Drone, Cargo
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
            if self.drone.is_holding:
                self.drone.is_holding = False
                self.drone.attached_cargo = None
            else:
                for other in self.drone.collision_list:
                    rope_length = float('inf')
                    attached_cargo = None
                    if isinstance(other, Cargo):
                        distance = self.drone.anchor_point.distance_to(other.transform.position)
                        if distance <= rope_length:
                            self.drone.is_holding = True
                            rope_length = distance
                            attached_cargo = other
                    self.drone.rope_length = rope_length
                    self.drone.attached_cargo = attached_cargo
                        

        if InputManager.is_key_down(pygame.K_e):
            self.drone.rope_length += self.drone.rope_speed * dt
        
        if InputManager.is_key_down(pygame.K_q):
            self.drone.rope_length -= self.drone.rope_speed * dt

        self.drone.set_thrust(left_input, right_input)

    def __str__(self):
        return "기본 조종기"
        
