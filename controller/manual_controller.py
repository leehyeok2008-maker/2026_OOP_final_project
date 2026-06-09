import pygame
from config import *
from controller.controller import Controller

class ManualController(Controller):
    def command(self, inputs) -> list[str]:
        commands = []
        for input in inputs:
            if input == KEY_W or input == KEY_UP:
                commands.append("MOVE_UPWARD")
            if input == KEY_S or input == KEY_DOWN:
                commands.append("MOVE_DOWNWARD")
            if input == KEY_A or input == KEY_LEFT:
                commands.append("MOVE_LEFT")
            if input == KEY_D or input == KEY_RIGHT:
                commands.append("MOVE_RIGHT")
        return commands            
                
