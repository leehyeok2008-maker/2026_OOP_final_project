import pygame
from config import *
from input import Input
from entities.drone import Drone
from controller.controller import Controller

class ManualController(Controller):
    def command(self, inputs):
        commands = [] 
        if Input.is_key_down(pygame.K_a) or Input.is_key_down(pygame.K_LEFT):
            commands.append("MOVE_LEFT")
        if Input.is_key_down(pygame.K_d) or Input.is_key_down(pygame.K_RIGHT):
            commands.append("MOVE_RIGHT")
        if Input.is_key_down(pygame.K_w) or Input.is_key_down(pygame.K_UP):
            commands.append("MOVE_UP")
        if Input.is_key_down(pygame.K_d) or Input.is_key_down(pygame.K_DOWN):
            commands.append("MOVE_DOWN")
        self.drone.add_commands(commands)
        
