import math
import matplotlib.pyplot as plt
from .controller import Controller
from .pid_controller import PIDController
from entities.drone import Drone, Cargo
from managers import InputManager
import pygame

class PIDManualController(Controller):
    def __init__(self, drone: Drone):
        super().__init__(drone)
        

        self.pid_y = PIDController(kp=15.0, ki=2.0, kd=8.0)
        self.pid_angle = PIDController(kp=20.0, ki=1.0, kd=10.0)

        self.target_y = self.drone.transform.position.y
        self.was_moving = False

    def command(self, dt: float, **kwargs):
        grav_acc = kwargs.get("grav_acc", 9.8)
        mass = self.drone.rigidbody.mass

        left_input = 0.0
        right_input = 0.0
        do_move = False
        
        if InputManager.is_key_down(pygame.K_w) or InputManager.is_key_down(pygame.K_UP):
            if self.drone.attached_cargo:
                left_input += self.drone.max_left_thrust
                right_input += self.drone.max_right_thrust
            else: 
                left_input += self.drone.max_left_thrust * 0.8
                right_input += self.drone.max_right_thrust * 0.8
            do_move = True
            
        if InputManager.is_key_down(pygame.K_a) or InputManager.is_key_down(pygame.K_LEFT):
            left_input += self.drone.max_left_thrust * 0.3
            right_input += self.drone.max_right_thrust * 0.7
            do_move = True
            
        if InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_RIGHT):
            left_input += self.drone.max_left_thrust * 0.7
            right_input += self.drone.max_right_thrust * 0.3
            do_move = True

        if InputManager.is_key_down(pygame.K_s) or InputManager.is_key_down(pygame.K_DOWN):
            left_input += self.drone.max_left_thrust * 0.2
            right_input += self.drone.max_right_thrust * 0.2
            do_move = True

        #region 로프 액션
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
        
        if do_move:
            self.pid_y.reset()
            self.pid_angle.reset()
            self.drone.set_thrust(left_input, right_input)
            self.was_moving = True
        else:
            if self.was_moving:
                braking_distance = self.drone.rigidbody.velocity.y * 0.15
                self.target_y = self.drone.transform.position.y + braking_distance
                self.was_moving = False

            out_y = self.pid_y.compute(self.target_y, self.drone.transform.position.y, dt)
            out_angle = self.pid_angle.compute(0, self.drone.transform.angle, dt)
            
            if self.drone.is_holding and self.drone.attached_cargo is not None:
                mass += self.drone.attached_cargo.rigidbody.mass
            total_thrust = out_y + mass * grav_acc
            left_thrust = (total_thrust / 2.0) - out_angle
            right_thrust = (total_thrust / 2.0) + out_angle

            self.drone.set_thrust(left_thrust, right_thrust)
        #endregion

    def __str__(self):
        return "PID 조종기"